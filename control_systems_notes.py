import control as ct
import numpy as np
import matplotlib.pyplot as plt

# LTI SYSTEM REPRESENTATION
# TRANSFER FUNCTIONS ARE DEFINED AS:
# G(s) = N(s)/D(s)
# WHERE N(s) AND D(s) ARE POLYNOMIALS IN s
#JUST LIKE IN MATLAB, THE COEFFICIENTS ARE GIVEN AS LISTS, WITH THE HIGHEST ORDER COEFFICIENT FIRST.
G = ct.tf([1], [1, 2, 1])
print(G)

# YOU CAN ALSO DO STATE SPACE SYSTEMS LIKE IN MATLAB
# WHERE A,B,C,D ARE THE STATE SPACE MATRICES.
# sys = ct.ss(A,B,C,D)

# FREQUENCY RESPONSE METHODS
# BODE PLOTS
# ct.bode(G)
# plt.show()
# YOU CAN ALSO SPECIFY THE FREQUENCY RANGE
# ct.bode(G, np.logspace(-2, 2))
# plt.show()

# YOU CAN GET THE FREQUENCY RESPONSE DATA INTO A TUPLE WITH FOLLOWING SYNTAX:
mag, phase, omega, = ct.frequency_response(G) # it will take in either SS or TF objects as the sys argument.

# you can also convert between the two representations as follows
# G = ct.ss2tf(sys)
# sys = ct.tf2ss(G)

# https://python-control.readthedocs.io/en/0.9.3.post2/control.html
