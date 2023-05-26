#step 1: import libraries
import numpy as np
import scipy.io as sio
from tqdm import tqdm
# Initialize smaller versions of the variables.
data = sio.loadmat('DemoModel.mat')
modl = data['Modl']
k_param = data['Props_k']
rho = data['Props_rho']
cp = data['Props_cp']
w = data['Props_w']
# Now convert the model to integers instead of floats.

# modl = np.array()
nx,ny,nz = modl.shape
wType = 1
# Here is the code that I need to make more efficient. I need to vectorize the for loops.
k1 = np.zeros((nx,ny,nz),dtype=np.float32)
rho_m = np.zeros((nx,ny,nz),dtype=np.float32)
cp_m = np.zeros((nx,ny,nz),dtype=np.float32)
operate_on_w_m = False
if wType==1:
    w_m = np.zeros((nx,ny,nz),dtype=np.float32)
    operate_on_w_m = True
# Use a for loop to fill in matrices with appropriate values from the input vectors.
for i in tqdm(range(nx),desc='Filling in matrices k1, rho, cp, and w_m'):
    for j in range(ny):
        for k in range(nz):
            x = modl[i,j,k]
            x = int(x)
            x-=1
            k1[i,j,k] = k_param[0][x]
            rho_m[i,j,k] = rho[0][x]
            cp_m[i,j,k] = cp[0][x]
            if operate_on_w_m:
                w_m[i,j,k] = w[0][x]

# Now do the same operations, but with the vectorized version of the code.
modl2 = data['Modl']
modl2 = modl2.astype(int)
modl2-=1
nx,ny,nz = modl2.shape

k1_v2 = np.zeros((nx,ny,nz),dtype=np.float32)
rho_m_v2 = np.zeros((nx,ny,nz),dtype=np.float32)
cp_m_v2 = np.zeros((nx,ny,nz),dtype=np.float32)

k1_v2[:,:,:] = k_param[0][modl2[:,:,:]]
rho_m_v2[:,:,:] = rho[0][modl2[:,:,:]]
cp_m_v2[:,:,:] = cp[0][modl2[:,:,:]]
w_m_v2 = np.zeros((nx,ny,nz),dtype=np.float32)
w_m_v2[:,:,:] = w[0][modl2[:,:,:]]
# Now compare the two versions of the code.

from var_checking_func import variable_checker

dict_data1 = {'k1': k1, 'rho_m': rho_m, 'cp_m': cp_m, 'w_m': w_m}
dict_data2 = {'k1': k1_v2, 'rho_m': rho_m_v2, 'cp_m': cp_m_v2, 'w_m': w_m_v2}
diff_dict = {}
for key in dict_data1.keys():
    diff_dict[key] = variable_checker(dict_data1[key], dict_data2[key], key)
