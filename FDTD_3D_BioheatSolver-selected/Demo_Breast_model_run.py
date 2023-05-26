import numpy as np
import scipy.io as sio
from Calc_TEMS_v045_python import calc_TEMPS_v045
import matplotlib.pyplot as plt

matlab_data = sio.loadmat('DemoBreastModel.mat')
Modl = matlab_data['Modl']
#convert model to integers instead of doubles
Modl = Modl.astype(int)
Modl = Modl -1 #MATLAB is 1-indexed, python is 0-indexed
Vox = matlab_data['Vox']
Vox = Vox/1000

t0 = np.zeros((Modl.shape))
dt = np.array(0.05) #seconds
path = matlab_data['path']
ht = np.array([path[:][-3]]) 
ct = np.array([path[:][-2]])
wType = np.array(1) # for uniform perfusion
tacq = np.array(1)
Tb = np.array(1)
Bc = np.array(0) #Adiabatic
rho = matlab_data['Props_rho']
c = matlab_data['Props_rho']
Q_s = matlab_data['Q']
cp = matlab_data['Props_cp']
k = matlab_data['Props_k']
w = matlab_data['Props_w']
nFZ = np.array(3)



(Temps, function_time) = calc_TEMPS_v045(Modl,t0,Vox, dt, ht,ct,rho,k,cp,wType,w,Q_s,nFZ,tacq, Tb, Bc)
# sio.savemat('py_vars_to_check.mat', {'time': function_time, 'TEMPS':Temps})
# plt.plot(function_time, np.squeeze(Temps[70,70,59,:]))
# plt.show()

