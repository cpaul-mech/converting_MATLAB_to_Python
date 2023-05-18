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
# import matplotlib.pyplot as plt
# import control as ct
import math
import tic_toc_generator as ttg
# matlab_data = sio.loadmat('DemoModel.mat')

def calc_TEMPS_v045(modl,T0,Vox,dt,HT,CT,rho,k_param,cp,wType,w,Q,nFZ,tacq,Tb,BC,temp_file=None):
    dx,dy,dz = Vox[0][0],Vox[0][1],Vox[0][2] # Voxel dimensions
    a = dx/dy                       # Dimensionless Increment NEEDED TO CHANGE TO LOWERCASE TO LET PYTHON KNOW IT IS NOT A CONSTANT.
    b = dx/dz                       # Dimensionless Increment
    nx,ny,nz = modl.shape           # Itentify number of voxels.
    t_final = np.sum(HT) + np.sum(CT)     # Total treatment time to be modeled. [s].
    time = np.arange(0,t_final,tacq) # Time vector
    NT = t_final/dt                 # Total number of FD time steps
    nntt = len(time)                # Total number of temperature distributions in time to save
    timeratio = tacq/dt             # NOTE: tacq/dt should be an integer

    # Calculate the maximum time step for stability of the thermal model
    w_max = w.max()               # Required parameters for max time step calculation
    rho_min = int(rho.min())           # Required parameters for max time step calculation
    cp_min = int(cp.min())             # Required parameters for max time step calculation
    k_max = k_param.max()        # Required parameters for max time step calculation
    dt_max = 1/(w_max/rho_min+2.0*k_max*(1.0+a**2+b**2)/(rho_min*cp_min*(dx**2)))  # Maximum allowable time step before iterations become unstable (s)
    if dt>dt_max:
        raise ValueError('Time step ''dt'' is too large for stable finite-difference calculations. Reduce ''dt'' and try again.')
    # ----------------------------------------
    # Create Matrices of Properties
    # ----------------------------------------
    k1 = np.zeros((nx,ny,nz),dtype=np.float32)
    k1[:,:,:] = k_param[modl[:,:,:]] #MAYBE USE LIST comprehension to accomplish this?
    k1 = 
    inv_k1 = 1/k1

    rho_m = np.zeros((nx,ny,nz),dtype=np.float32)
    rho_m[:,:,:] = rho[modl[:,:,:]]

    cp_m = np.zeros((nx,ny,nz),dtype=np.float32)
    cp_m[:,:,:] = cp[modl[:,:,:]]

    if wType==1:
        w_m = np.zeros((nx,ny,nz),dtype=np.float32)
        w_m[:,:,:] = w[modl[:,:,:]]
    elif wType==2:
        w_m = w
        del w
    
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
        +a**2/(inv_k4k1)+a**2/(inv_k5k1)    # y direction conduction (W/m/degC)
        +b**2/(inv_k6k1)+b**2/(inv_k7k1))     # z direction conduction (W/m/degC)
    Coeff2 = (1-(w_m*dt)/rho_m-2*dt/(rho_cp*dx**2)*k8) # Changes associated with this voxel's old temperature (Unitless)
    Perf=(w_m*dt*Tb)/rho_m # Precalculate perfusion term (degC)

    j = nx+1                                 # second to last voxel in direction X #otherwise we can change this to nx+2 to account for python list slicing not including final option.
    k_var = ny+1                                 # second to last voxel in direction Y
    l = nz+1                                 # second to last voxel in direction Z

    # ----------------------------------------
    # Solver
    # ----------------------------------------
    
    TicToc = ttg.TicTocGenerator() # create an instance of the TicTocGen generator
    tic = ttg.tic
    toc = ttg.toc
    tic()   # Starts the stopwatch
    # h = 0 # Initiate waitbar MAY NOT HAVE FUNCTIONALITY
    c_old = 1    # counter
    # Preallocate temperature arrays
    T_old = np.zeros((nx+2,ny+2,nz+2),dtype=np.float32)   # Define Old Temperatures ***NOTE: Expanded by 2 voxels in x y and z direction
    # Initial Condition
    T_old[1:j,1:k_var,1:l] = T0              # Fill in initial condition temperatures.

    # Boundary Condition
    if BC==1:                           # Adiabatic boundary condition (zero-slope)
        T_old[0,   1:k_var, 1:l] = T0[0,:,:]
        T_old[-1, 1:k_var, 1:l] = T0[-1,:,:]
        T_old[1:j, 0,   1:l] = T0[:,0,:]
        T_old[1:j, -1, 1:l] = T0[:,-1,:]
        T_old[1:j, 1:k_var, 0  ] = T0[:,:,0]
        T_old[1:j, 1:k_var, -1] = T0[:,:,-1]
    elif BC==2:                       # Matching Slope Boundary (slope between edge and 2nd voxel matches slope between 2nd and 3rd voxel)
        T_old[0,:,:] = T_old[1,:,:]-(T_old[2,:,:]-T_old[1,:,:])
        T_old[-1,:,:] = T_old[-2,:,:]-(T_old[-3,:,:]-T_old[-2,:,:])
        T_old[:,0,:] = T_old[:,1,:]-(T_old[:,2,:]-T_old[:,1,:])
        T_old[:,-1,:] = T_old[:,-2,:]-(T_old[:,-3,:]-T_old[:,-2,:])
        T_old[:,:,0] = T_old[:,:,1]-(T_old[:,:,2]-T_old[:,:,1])
        T_old[:,:,-1] = T_old[:,:,-2]-(T_old[:,:,-3]-T_old[:,:,-2])
    
    T_new = T_old                            # Define new temperatures

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
        TEMPS = 0 #dummy value to return
    else:
        TEMPS = np.zeros((nx,ny,nz,nntt),dtype=np.float32)   # Final exported array
        TEMPS[:,:,:,0] = T0

    for mm in range(nFZ):                                # Run Model for each focal zone location
        # Generate the PowerOn vector for each focal zone location (includes heating and cooling time)
        nt = math.ceil(HT[mm]/dt)+math.ceil(CT[mm]/dt) # Number of time steps at FZ location mm
        PowerOn = np.zeros(nt)                # Zero indicates no power.
        PowerOn[0:math.ceil(HT[mm]/dt)] = 1       # 1 indicates power on.
        Qmm = Q[:,:,:,mm]                 # Power deposited at FZ location mm
        for nn in range(nt):                             # Run Model for each timestep at FZ location mm
            cc = c_old                           # Counter starts at 1 (line 120)
            c_old = cc+1                         # Counter increments by 1 each iteration
            # waitbar(cc/NT,h)                   # Increment the waitbar
            # Shift Temperatures for use in solver
            t2 = np.roll(T_new,1,axis=0)
            t3 = np.roll(T_new,-1,axis=0)
            t4 = np.roll(T_new,1,axis=1)
            t5 = np.roll(T_new,-1,axis=1)
            t6 = np.roll(T_new,1,axis=2)
            t7 = np.roll(T_new,-1,axis=2)
            # Solve for Temperature of Internal Nodes  (TEMPS_new = New Temperature)
            ###### NEED TO VERIFY THAT LIST SLICING IN PYTHON WORKS IN THIS INSTANCE EQUIVALENTLY TO MATLAB. see line 290 ######
            T_new[1:j,1:k_var,1:l] = np.squeeze(Coeff1*                                                      # Conduction associated with neighboring voxels
                                                (t2[1:j,1:k_var,1:l]/(inv_k2k1)+t3[1:j,1:k_var,1:l]/(inv_k3k1)      # x direction conduction 
                                                +a**2*(t4[1:j,1:k_var,1:l]/(inv_k4k1)+t5[1:j,1:k_var,1:l]/(inv_k5k1))      # y direction conduction
                                                +Perf                                                          # Perfusion associated with difference between baseline and Tb temperature
                                                +Qmm*PowerOn[nn]*dt/rho_cp                                   # FUS power
                                                +T_old[1:j,1:k_var,1:l]*Coeff2))                                       # Temperature changes associated with this voxel's old temperature
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
                    TEMPS[:,:,:,cc/timeratio] = T_new[1:j,1:k_var,1:l]
        if use_file:
            fid.close()
    #create list of items to be deleted.
    k2,k3,k4,k5,k6,k7 = 0,0,0,0,0,0
    del_items = [T_new, T_old, t2, t3, t4, t5, t6, t7, k1, k2, k3, k4, k5, k6, k7, w_m, rho_m, cp_m, rho_cp]
    #delete items
    for item in del_items:
        del item
    toc()   # Stops the stopwatch

    return TEMPS, time
