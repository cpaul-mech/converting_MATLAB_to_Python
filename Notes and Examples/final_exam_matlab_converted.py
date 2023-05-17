import control as ct
import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
a = np.array([1, 14, 58])
roots_a = np.roots(a)
print(roots_a) # it works just like in MATLAB!!
numerator = [4]
denom = [1, 14, 58]
sys = ct.tf(numerator, denom)
# help(ct.step_response)
t, y = ct.step_response(sys)
# plt.plot(t, y)
# plt.show()

"""
convert the following matlab code to python:
sys16 = tf(1, [1 .5 1]);
sys17 = tf(25, [1 10 25]);
sys18 = tf(25, [1 2.5 25]);
sys19 = tf(5, [1 5]);
sys20 = tf(1, [1 2 1]);
sys21 = tf(1, [1 1]);
h = bodeplot(sys16, sys17, sys18, sys19, sys20, sys21)
legend("sys16","sys17","sys18","sys19", "sys20","sys21")
setoptions(h, 'MagUnits', 'abs','FreqScale','linear','XLim', {[0 10]})
"""
sys16 = ct.tf(1, [1, .5, 1])
sys17 = ct.tf(25, [1, 10, 25])
sys18 = ct.tf(25, [1, 2.5, 25])
sys19 = ct.tf(5, [1, 5])
sys20 = ct.tf(1, [1, 2, 1])
sys21 = ct.tf(1, [1, 1])
omega_vector = np.linspace(0, 10, 1000)
sys_list = [sys16, sys17, sys18, sys19, sys20, sys21]
# h_test = ct.bode_plot(sys16)
mag, phase, omega = ct.bode_plot(sys_list, Hz = False, deg = True, omega = omega_vector, plot= False)
# plt.legend(["sys16", "sys17", "sys18", "sys19", "sys20", "sys21"])
# plt.show()
# convert phase from radians to degrees
for i in range(len(phase)):
    for j in range(len(phase[i])):
        phase[i][j] = phase[i][j] * (180/np.pi)
# plot the magnitude and phase
plot = plt.figure(1, figsize=(8, 6), dpi=100)
mag_plot = plot.add_subplot(2,1,1)
phase_plot = plot.add_subplot(2,1,2)
for i in range(len(mag)):
    mag_plot.plot(omega[i], mag[i], label = "sys" + str(i+16))
for i in range(len(phase)):
    phase_plot.plot(omega[i], phase[i], label = "sys" + str(i+16))
#show the legend
mag_plot.set_title("Bode Plot")
mag_plot.legend()
phase_plot.set_xlabel("Frequency (rad/s)")
mag_plot.set_ylabel("Magnitude Ratio")
phase_plot.set_ylabel("Phase (deg)")
phase_plot.legend()
#show the plot
plt.savefig("bode_plot.svg")
plt.show()

# we can plot the poles of the system as follows:
poles_list = []
Poles_plot = plt.figure(1, figsize=(8, 6), dpi=100)
poles_plot_axis = Poles_plot.add_subplot(1,1,1)

for i in range(len(sys_list)):
    poles = ct.pole(sys_list[i])
    poles_list.append(poles)
    poles_plot_axis.plot(np.real(poles), np.imag(poles), 'x', label = "sys" + str(i+16))

poles_plot_axis.set_title("Poles")
poles_plot_axis.set_xlabel("Real")
poles_plot_axis.set_ylabel("Imaginary")
poles_plot_axis.grid()
#Now add vertical and horizontal lines at 0 to show the axes
poles_plot_axis.axvline(x=0, color='k')
poles_plot_axis.axhline(y=0, color='k')
poles_plot_axis.legend()
plt.show()

