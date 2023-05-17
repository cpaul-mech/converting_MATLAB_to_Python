# Differential equations are solved in python using the scipy.integrate package using the odeint function or the solve_ivp function.
# odeint is a wrapper around the Fortran library odepack, which is a collection of numerical routines for solving systems of ordinary differential equations.
# solve_ivp is a wrapper around the Fortran library odepack, which is a collection of numerical routines for solving systems of ordinary differential equations.

""" Another Python package that solves differential equations is GEKKO. GEKKO is a Python package for 
machine learning and optimization of mixed-integer and differential algebraic equations. It is coupled 
with large-scale solvers for linear, quadratic, nonlinear, and mixed integer programming (LP, QP, NLP, MILP, MINLP). 
Modes of operation include parameter regression, data reconciliation, real-time optimization, dynamic simulation, and 
nonlinear predictive control."""

# Importing the required libraries
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

# function that returns dy/dt
def model(y,t):
    k = 0.3
    dydt = -k * y
    return dydt

# initial condition
y0 = 5

# time points
t,step = np.linspace(0,20,retstep= True)
print(f"t_step: {step}")

# solve ODE
y = odeint(model,y0,t)

# plot results
plt.plot(t,y)
plt.xlabel('time')
plt.ylabel('y(t)')
plt.show()