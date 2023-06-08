# This file is meant to have the same functionality as the matlab file Calc_TEMS_v045.m
# -------- Function Name ---------------------------------------------- 
# Calc_TEMPS_v04S.m
# -------- Purpose --------
# Finite-difference thermal solver with non-homogeneous thermal properties, 
# Pennes perfusion model, and heating source defined by Q variable.
# -------- Input Data --------
#   Modl                [nX,nY,nZ]. Segemented tissue model (ie.  1=water, 2=fat, 3...nTypes)
#   T0                  [nX,nY,nZ]. Initial temperature condition relative to baseline. [deg C].
#   Vox                 1x3 vector. Voxel dimensions [dy dx dz]. [m].
#   dt                  Scalar. Time step for thermal solver. [s].
#   HT                  1xnFZ vector. Heating time at each FZ location. [s].
#   CT                  1xnFZ vector. Cooling time at each FZ location. [s].
#   rho                 1xnTypes. Density. [kg/m^3]. 
#   k                   1xnTypes. Thermal conductivity. [W/(m*deg C)]. 
#   c                   1xnTypes. Specific heat capacity. [J/(kg*deg C)]. 
#   wType               '1'==Uniform perfusion; '2'==Local perfusion;
#   w                       if wType=1--> 1xnTypes. Tissue type uniform Pennes perfusion. [kg/(m^3*s)]. 
#                           if wType=2--> [nX,nY,nZ]. Local voxel by voxel Pennes perfusion. [kg/(m^3*s)].
#   Q                   [nX,nY,nZ,nFZ]. Q patterns for each focal zone. [W/m^3].
#                           NOTE: Q=rho*SAR. [W/m^3]=[kg/m^3]*[W/kg].
#   nFZ                 Scalar. Number of Focal Zone Locations.
#   tacq                Scalar. Final time resolution of temperatures. [s].
#                           NOTE: 'dt' should divide evenly into 'tacq'.
#   Tb                  Scalar. Arterial blood temperature for perfusion. [deg C].
#                           NOTE: Measured relative to baseline, typically 0 deg C.
#   BC                  '0' for zero temperature boundary condition. 
#                       '1' for adiabatic boundary condition. 
#                       '2' for matching slope boundary condition.
#   temp_file           (optional) A file for writing the temperatures to.
#                       For data sets which involve a large number of time
#                       points (i.e. enough that all the memory will be
#                       consumed), writing to a file will prevent memory
#                       thrashing and speed the program up.
# -------- Output Data --------
#   TEMPS               4D finite-difference temperature array
#   time                time vector associated with TEMPS array
# -------- Required Subfunctions --------
#       NA
# -------- Author Info --------
#       Christopher Dillon
#       Department of Bioengineering
#       University of Utah
#       Version 01: 28 September 2010
# -------- Updates --------
#       v02      30 Nov 2011        # Introduced 'timeratio' variable to save data every timeratio-th FD step
#       v03      12 Apr 2014        # Introduced 'T0', nonuniform initial condition
#                                   # Replaced 'timeratio' variable with 'tacq'
#       v04      18 Jul 2014        # Commented and cleaned up code
#                                   # Reintroduced stability criterion
#                                   # Replaced 'SAR' with 'Q'
#                                   # Introduced Adiabatic and Matching Slope boundary conditions
#                                   # Introduced option for local perfusion
#       v04S     05 Jan 2015        # (Scott Almquist) improved the run time by precalculating any
#                                      constant matrices and added option to write to a file (see
#                                      helper function read_temp_file.m)

import numpy as np
import scipy.io as sio
# matlab_data = sio.loadmat('DemoModel.mat')
from tqdm import tqdm
import time
def calc_TEMPS_v04S(modl,T0,Vox,dt,HT,CT,rho,k_param,cp,wType,w,Q,nFZ,tacq,Tb,BC,temp_file=None):
    program_start = time.time()
    dx,dy,dz = Vox[0][0],Vox[0][1],Vox[0][2] # Voxel dimensions
    # Since a and b are only ever used when they're squared, we can just square them here.
    a = (dx/dy)**2                        # Dimensionless Increment
    b = (dx/dz)**2                        # Dimensionless Increment
    nx,ny,nz = modl.shape                 # Itentify number of voxels.
    t_final = np.sum(HT)+np.sum(CT)       # Total treatment time to be modeled. [s].
    time_vector = np.arange(0,t_final+1,tacq) # Time vector
    nntt = len(time_vector)               # Total number of temperature distributions in time to save

    timeratio = tacq/dt                    # NOTE: tacq/dt should be an integer
    if int(timeratio) == timeratio:        # Check if tacq/dt is an integer stored as a double, like 20.0
        timeratio = int(timeratio)         # If so, convert to an integer, like 20
    else:
        raise ValueError('tacq/dt must be an integer. Please change tacq or dt and try again.')
    # Calculate the maximum time step for stability of the thermal model
    w_max = w.max()                  # Required parameters for max time step calculation
    rho_min = int(rho.min())         
    cp_min = int(cp.min())           
    k_max = k_param.max()            
    dt_max = 1/(w_max/rho_min+2.0*k_max*(1.0+a+b)/(rho_min*cp_min*(dx**2)))  # Maximum allowable time step before iterations become unstable (s)
    if dt>dt_max:
        raise ValueError('Time step ''dt'' is too large for stable finite-difference calculations. Reduce ''dt'' and try again.')
    # ----------------------------------------
    # Create Matrices of Properties
    # ----------------------------------------
    # Create empty matrices.
    k1 = np.zeros((nx,ny,nz),dtype=np.float32)
    rho_m = np.zeros((nx,ny,nz),dtype=np.float32)
    cp_m = np.zeros((nx,ny,nz),dtype=np.float32)
    # Populate matrices with values from model.
    k1[:,:,:] = k_param[0][modl[:,:,:]]
    rho_m[:,:,:] = rho[0][modl[:,:,:]]
    cp_m[:,:,:] = cp[0][modl[:,:,:]]
    
    if wType==1:
        w_m = np.zeros((nx,ny,nz),dtype=np.float32)
        w_m[:,:,:] = w[0][modl[:,:,:]]
    elif wType==2:
        w_m = w
        del w
    # Calculate inverse of k1 for use in solver
    inv_k1 = 1/k1
    
    rho_cp = rho_m*cp_m                       # Simplfies later equations by combining density and specific heat

    # Shift k values for use in solver
    inv_k2k1 = 1/np.roll(k1,1,axis=0) + inv_k1  # (m*degC/W)
    inv_k3k1 = 1/np.roll(k1,-1,axis=0) + inv_k1
    inv_k4k1 = 1/np.roll(k1,1,axis=1) + inv_k1
    inv_k5k1 = 1/np.roll(k1,-1,axis=1) + inv_k1
    inv_k6k1 = 1/np.roll(k1,1,axis=2) + inv_k1
    inv_k7k1 = 1/np.roll(k1,-1,axis=2) + inv_k1

    Coeff1 = 2*dt/(rho_cp*dx**2)                # (m*degC/W)
    k8 = (1/(inv_k2k1)+1/(inv_k3k1)          # x direction conduction (W/m/degC)
        +a/(inv_k4k1)+a/(inv_k5k1)     # y direction conduction (W/m/degC)
        +b/(inv_k6k1)+b/(inv_k7k1))    # z direction conduction (W/m/degC)
    Coeff2 = (1-(w_m*dt)/rho_m-2*dt/(rho_cp* dx**2)*k8) # Changes associated with this voxel's old temperature (Unitless)
    Perf=(w_m*dt*Tb)/rho_m # Precalculate perfusion term (degC) 

    j = -1                                 # second to last voxel in direction X 
    k_var = -1                             # second to last voxel in direction Y
    l = -1                                 # second to last voxel in direction Z
    
    # ----------------------------------------
    # Solver
    # ----------------------------------------
    
    
    c_old = 1    # counter
    # Preallocate temperature arrays
    T_old = np.zeros((nx+2,ny+2,nz+2),dtype=np.float32)   # Define Old Temperatures ***NOTE: Expanded by 2 voxels in x y and z direction
    # Initial Condition
    
    T_old[1:j,1:k_var,1:l] = T0              # Fill in initial condition temperatures.

    # Boundary Condition
    if BC==1:                           # Adiabatic boundary condition (zero-slope)
        T_old[0,   1:k_var, 1:l] = T0[0,:,:]
        T_old[-1,  1:k_var, 1:l] = T0[-1,:,:]
        T_old[1:j,       0, 1:l] = T0[:,0,:]
        T_old[1:j,      -1, 1:l] = T0[:,-1,:]
        T_old[1:j, 1:k_var,  0] = T0[:,:,0]
        T_old[1:j, 1:k_var, -1] = T0[:,:,-1]
    elif BC==2:                       # Matching Slope Boundary (slope between edge and 2nd voxel matches slope between 2nd and 3rd voxel)
        T_old[0,:,:] = T_old[1,:,:]-(T_old[2,:,:]-T_old[1,:,:])
        T_old[-1,:,:] = T_old[-2,:,:]-(T_old[-3,:,:]-T_old[-2,:,:])
        T_old[:,0,:] = T_old[:,1,:]-(T_old[:,2,:]-T_old[:,1,:])
        T_old[:,-1,:] = T_old[:,-2,:]-(T_old[:,-3,:]-T_old[:,-2,:])
        T_old[:,:,0] = T_old[:,:,1]-(T_old[:,:,2]-T_old[:,:,1])
        T_old[:,:,-1] = T_old[:,:,-2]-(T_old[:,:,-3]-T_old[:,:,-2])
    
    T_new = T_old                          # Define new temperatures

    # Initial temperature profile
    use_file = 0

    if isinstance(temp_file, str):
        use_file = 1
        try:
            fid = open(temp_file, 'w')
            fid.write(nx)
            fid.write(ny)
            fid.write(nz)
            fid.write(nntt)
            fid.write(T0)
        except:
            print("Could not open file! Please close Excel!")
            # stop execution of the program
            raise 
        Temps = 0 #dummy value to return
    else:
        Temps = np.zeros((nx,ny,nz,nntt),dtype=np.float32)   # Final exported array
        Temps[:,:,:,0] = T0
    for mm in range(int(nFZ)):                                # Run Model for each focal zone location
        # Generate the PowerOn vector for each focal zone location (includes heating and cooling time)
        nt = np.ceil(HT[mm]/dt)+np.ceil(CT[mm]/dt) # Number of time steps at FZ location mm
        nt = int(nt)
        PowerOn = np.zeros((nt,1),dtype=np.int8)  # Zero indicates no power.
        z = np.ceil(HT[mm]/dt)
        z = int(z)
        PowerOn[0:z,:] = 1             # 1 indicates power on.
        #checking if Q has 4 dimensions
        if Q.ndim ==4:
            Qmm = np.zeros((nx,ny,nz),dtype=np.float32)   # Define Q for each focal zone location
            Qmm[:,:,:] = Q[:,:,:,mm]
        else:
            Qmm = Q[:,:,:]
        # tqdm(range(nt), desc=f'Running model for each timestep at FZ location {mm}')
        for nn in tqdm(range(nt), desc=f'Running model for each timestep at FZ location {mm}'):    # Run Model for each timestep at FZ location mm
            cc = c_old                           # Counter starts at 1 (line 120)
            c_old = cc+1                         # Counter increments by 1 each iteration
            # Shift Temperatures for use in solver
            t2 = np.roll(T_new,1,axis=0)
            t3 = np.roll(T_new,-1,axis=0)
            t4 = np.roll(T_new,1,axis=1)
            t5 = np.roll(T_new,-1,axis=1)
            t6 = np.roll(T_new,1,axis=2)
            t7 = np.roll(T_new,-1,axis=2)
            
            # Solve for Temperature of Internal Nodes  (TEMPS_new = New Temperature)
            x_dir_cond = t2[1:j,1:k_var,1:l]/(inv_k2k1)+t3[1:j,1:k_var,1:l]/(inv_k3k1)         # x direction conduction (W/m/degC)
            y_dir_cond = (a)*(t4[1:j,1:k_var,1:l]/(inv_k4k1)+t5[1:j,1:k_var,1:l]/(inv_k5k1))   # y direction conduction (W/m/degC)
            z_dir_cond = (b)*(t6[1:j,1:k_var,1:l]/(inv_k6k1)+t7[1:j,1:k_var,1:l]/(inv_k7k1))   # z direction conduction (W/m/degC)
            # sample =  # Temperature changes associated with this voxel's old temperature (degC)
            T_new[1:j,1:k_var,1:l] = np.squeeze(Coeff1*(x_dir_cond+y_dir_cond+z_dir_cond)+Perf+Qmm*PowerOn[nn]*dt/rho_cp+T_old[1:j,1:k_var,1:l]*Coeff2)
            
            # T_new[1:j,1:k_var,1:l] = np.squeeze(Coeff1*                                  # Conduction associated with neighboring voxels
            #                                  (x_dir_cond+y_dir_cond+z_dir_cond           # Conduction associated with neighboring voxels
            #                                  +Perf                                       # Perfusion associated with difference between baseline and Tb temperature  
            #                                  +Qmm*PowerOn[nn]*dt/rho_cp                  # FUS power
            #                                  +T_old[1:j,1:k_var,1:l]*Coeff2))            # Temperature changes associated with this voxel's old temperature
            
            # Make recently calculated temperature (T_new) the old temperature (T_old) for the next calculation
            T_old[1:j,1:k_var,1:l] = T_new[1:j,1:k_var,1:l]
            if BC==1:                           # Adiabatic Boundary
                T_old[0,:,:] = T_new[1,:,:]
                T_old[-1,:,:] = T_new[-2,:,:]
                T_old[:,0,:] = T_new[:,1,:]
                T_old[:,-1,:] = T_new[:,-2,:]
                T_old[:,:,0] = T_new[:,:,1]
                T_old[:,:,-1] = T_new[:,:,-2]
            elif BC==2:                       # Matching Slope Boundary
                T_old[0,:,:] = T_new[1,:,:]-(T_new[2,:,:]-T_new[1,:,:])
                T_old[-1,:,:] = T_new[-2,:,:]-(T_new[-3,:,:]-T_new[-2,:,:])
                T_old[:,0,:] = T_new[:,1,:]-(T_new[:,2,:]-T_new[:,1,:])
                T_old[:,-1,:] = T_new[:,-2,:]-(T_new[:,-3,:]-T_new[:,-2,:])
                T_old[:,:,0] = T_new[:,:,1]-(T_new[:,:,2]-T_new[:,:,1])
                T_old[:,:,-1] = T_new[:,:,-2]-(T_new[:,:,-3]-T_new[:,:,-2])
            
            if cc%timeratio==0:                 # Determine whether to save the current TEMPS or not
                if use_file:
                    fid.write(T_new[1:j,1:k_var,1:l])
                else:
                    index = int(cc/timeratio)
                    Temps[:,:,:,index] = T_new[1:j,1:k_var,1:l]
        if use_file:
            fid.close()
    # sio.savemat('py_vars_to_check.mat', {'c_old':c_old, 'T_new':T_new, 'PowerOn': PowerOn, 'T7':t7, 'time': time_vector, 'TEMPS':Temps,'k8':k8})
    # create list of items to be deleted.
    # del_items = [T_new, T_old, t2, t3, t4, t5, t6, t7, k1, w_m, rho_m, cp_m, rho_cp]
    # #delete items
    # for item in del_items:
    #     del item
    print(f'Model run completed in {time.time()-program_start:.2f} seconds. \n') # the .2f limits the number of decimals to 2
    return Temps, time_vector
