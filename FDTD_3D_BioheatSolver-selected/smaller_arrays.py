import numpy as np
import scipy.io as sio
import time
from Calc_TEMS_v045_python import calc_TEMPS_v045
"""
Convert the following MATLAB code into python code then run function.
load('DemoModel.mat')
% Need T0, initial temperature condition
% We say that everything starts at temperature of 0 for a datum.
T0 = zeros(size(Modl),'single');
%convert Vox to m, given in mm.
Vox = Vox/1000;
dt = 0.05; %seconds
%need HT and CT, same size as nFZ
HT = path(end-2); %or position 7
CT = path(end-1);
wType = 1; % for uniform perfusion
tacq = 1; % aquisition time.
Tb= 0; 
BC = 0; %adiabatic, no energy escapes out of the edges
% the file is optional. 

[TEMPS,time]=Calc_TEMPS_v04S(Modl,T0,Vox,dt,HT,CT,Props_rho,Props_k,Props_cp,wType,Props_w,Q,nFZ,tacq,Tb,BC);

plot(time,squeeze(TEMPS(71,71,60,:)))
%TO slice the model and look at temp distribution use the command imagesc()
imagesc(squeeze(TEMPS(71,:,:,11)),[0, 12])
"""
import control.matlab as control
import matplotlib.pyplot as plt
matlab_data = sio.loadmat('DemoModel.mat')
Modl = matlab_data['Modl']
#Slice Modl to make it much smaller. Lets try 10x10x10
# Modl = Modl[0:5,0:5,0:5]
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
# we also need to slice Q
# Q_s = Q_s[0:5,0:5,0:5]
cp = matlab_data['Props_cp']
k = matlab_data['Props_k']
w = matlab_data['Props_w']
nFZ = matlab_data["nFZ"]
GF = matlab_data['GF']


(Temps, function_time) = calc_TEMPS_v045(Modl,t0,Vox, dt, ht,ct,rho,k,cp,wType,w,Q_s,nFZ,tacq, Tb, Bc)
sio.savemat('py_vars_to_check.mat', {'time': function_time, 'TEMPS':Temps})
plt.plot(function_time, np.squeeze(Temps[70,70,59,:]))
plt.show()

