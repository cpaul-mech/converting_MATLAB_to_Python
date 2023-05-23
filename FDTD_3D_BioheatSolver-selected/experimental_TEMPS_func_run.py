import numpy as np
import scipy.io as sio
from Calc_TEMS_v045_python import calc_TEMPS_v045
import matplotlib.pyplot as plt

matlab_data = sio.loadmat('DemoModel.mat')
Modl = matlab_data['Modl']

Vox = matlab_data['Vox']
Vox = Vox/1000

t0 = np.zeros((Modl.shape))
dt = np.array(0.05) #seconds
path = matlab_data['path']
ht = np.array([path[0][-3]]) 
ct = np.array([path[0][-2]])
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
nFZ = matlab_data["nFZ"]
GF = matlab_data['GF']


(Temps, function_time) = calc_TEMPS_v045(Modl,t0,Vox, dt, ht,ct,rho,k,cp,wType,w,Q_s,nFZ,tacq, Tb, Bc)
# sio.savemat('py_vars_to_check.mat', {'time': function_time, 'TEMPS':Temps})
plt.plot(function_time, np.squeeze(Temps[70,70,59,:]))
plt.show()

