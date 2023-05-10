# This code shows an example of how to import and manipulate data from a .mat file
# Specifically, the data from the forced_response_data.mat file and the free_response_data.mat file in HW 12.

#this code will show how to import and manipulate data from the forced_response_data.mat file
# from os.path import dirname, join as pjoin
import numpy as np
import scipy.io as sio
# import pi 
from math import pi
#load the data from the .mat file

forced_response_data = sio.loadmat('forced_response_data.mat')
free_response_data = sio.loadmat('free_response_data.mat')
forced_response_data = forced_response_data['data']
free_response_data = free_response_data['data']
forced_response_data = np.array(forced_response_data)
free_response_data = np.array(free_response_data)
forced_response_data[:,1] = forced_response_data[:,1] * (2* pi/60) # convert rpm to rad/s
free_response_data[:,1] = free_response_data[:,1] * (2* pi/60) # convert rpm to rad/s

#  given
density = 2.8 * 10**3
diameter = .36
volume = pi * (diameter**2 / 4) * (6.35 / 1000)
mass = density * volume
massHole = (density * (pi * (16/1000)**2 / 4) * (6.35/1000))
# calculate intertia
I_hole = ((massHole * (16/1000)**2) / 8) + (0.165**2 * massHole)
I_disk = ((mass * (diameter)**2) / 8) - (I_hole * 30); # This is the intertia to use

# Plot forced response Data:
import matplotlib.pyplot as plt
forced_T = forced_response_data[:,0]
forced_w = forced_response_data[:,1]
forced_max = max(forced_w)
forced_63= 0.37 * forced_max
forced_63_index = np.where(forced_w > forced_63)
ForcedTau = 16.617196 - 5.577
forced_B = I_disk / ForcedTau
plt.plot(forced_T, forced_w, 'r-', linewidth=2, label='Forced Response')
plt.title('Forced Response Data')
plt.show()

