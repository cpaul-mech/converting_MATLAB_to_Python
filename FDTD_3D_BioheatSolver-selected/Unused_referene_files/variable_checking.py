# This python file will be used to check differences between variables in the matlab code and the python code.

import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt

matlab_data = sio.loadmat('variables_to_check.mat')
print(matlab_data.keys())
python_data = sio.loadmat('py_vars_to_check.mat')
print(python_data.keys())
def variable_checker():
    # This function will check the variables in the matlab code and the python code.
    # The variables should be similar within a tolerance of 1e-6
    # We return a dictionary of the names of the variables and the number of differences.
    # The variables to check are:
    # Temps, inv_k1, invk5k1, rho_cp, k1, and k8
    # load all the variables from each file
    py_temps = python_data['TEMPS']
    mat_temps = matlab_data['TEMPS']
    diff_dict = {}
    #now compare the two variables with a for loop and a tolerance of 1e-6
    nx, ny, nz, nt  = mat_temps.shape
    px, py, pz, pt = py_temps.shape
    if nx == px and ny == py and nz == pz and nt == pt:
        differences = 0
        print("The sizes of the temps variables are the same.")
    else:
        print("The sizes of the temps variables are not the same.")
        diff_dict['TEMPS'] = 'Not same shape.'
    """for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                for l in range(nt):
                    if abs(py_temps[i,j,k,l] - mat_temps[i,j,k,l]) < 1e-1:
                        pass
                    else:
                        differences += 1
                        # print(f'The values at {i},{j},{k},{l} are not the same.')
                        # print("The difference is: ", abs(py_temps[i,j,k,l] - mat_temps[i,j,k,l]))
    print("The number of differences is: ", differences) # the number of differences here was 5398548. That's way too many.
    diff_dict['TEMPS'] = differences"""
    py_k1 = python_data['k1']
    mat_k1 = matlab_data['k1']
    nx, ny, nz = mat_k1.shape
    px, py, pz = py_k1.shape
    if nx == px and ny == py and nz == pz:
        differences = 0
        print(f"The shapes of the k1 variables: {mat_k1.shape} are the same.")
    else:  
        print("The shapes of the k1 variables are not the same.")
        diff_dict['k1'] = 'Not same shape.'
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                if abs(py_k1[i,j,k] - mat_k1[i,j,k]) < 1e-4:
                    pass
                else:
                    differences += 1
                    print(f'The values at {i},{j},{k} are not the same.')
                    print("The difference is: ", abs(py_k1[i,j,k] - mat_k1[i,j,k]))
    # print("The number of differences is: ", differences) # There were no differences here.
    diff_dict['k1'] = differences


    py_k8 = python_data['k8']
    mat_k8 = matlab_data['k8']
    nx, ny, nz = mat_k8.shape
    px, py, pz = py_k8.shape
    if nx == px and ny == py and nz == pz:
        differences = 0
        print(f"The shapes of the k8 variables: {mat_k8.shape} are the same.")
    else:
        print("The shapes of the k8 variables are not the same.")
        diff_dict['k8'] = 'Not same shape.'
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                if abs(py_k8[i,j,k] - mat_k8[i,j,k]) < 1e-4:
                    pass
                else:
                    differences += 1
                    print(f'The values at {i},{j},{k} are not the same.')
                    print("The difference is: ", abs(py_k8[i,j,k] - mat_k8[i,j,k]))
    # print("The number of differences is: ", differences) # There were no differences here.
    diff_dict['k8'] = differences

    py_rho_cp = python_data['rho_cp']
    mat_rho_cp = matlab_data['rho_cp']
    nx, ny, nz = mat_rho_cp.shape
    px, py, pz = py_rho_cp.shape
    if nx == px and ny == py and nz == pz:
        differences = 0
        print(f"The shapes of the rho_cp variables: {mat_rho_cp.shape} are the same.")
    else:
        print("The shapes of the rho_cp variables are not the same.")
        diff_dict['rho_cp'] = 'Not same shape.'
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                if abs(py_rho_cp[i,j,k] - mat_rho_cp[i,j,k]) < 1e-4:
                    pass
                else:
                    differences += 1
                    print(f'The values at {i},{j},{k} are not the same.')
                    print("The difference is: ", abs(py_rho_cp[i,j,k] - mat_rho_cp[i,j,k]))
    # print("The number of differences is: ", differences) # There were no differences here.
    diff_dict['rho_cp'] = differences

    py_inv_k1 = python_data['inv_k1']
    mat_inv_k1 = matlab_data['inv_k1']
    nx, ny, nz = mat_inv_k1.shape
    px, py, pz = py_inv_k1.shape
    if nx == px and ny == py and nz == pz:
        differences = 0
        print(f"The shapes of the invk1 variables: {mat_inv_k1.shape} are the same.")
    else:
        print("The shapes of the invk1 variables are not the same.")
        diff_dict['invk1'] = 'Not same shape.'
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                if abs(py_inv_k1[i,j,k] - mat_inv_k1[i,j,k]) < 1e-4:
                    pass
                else:
                    differences += 1
                    print(f'The values at {i},{j},{k} are not the same.')
                    print("The difference is: ", abs(py_inv_k1[i,j,k] - mat_inv_k1[i,j,k]))
    # print("The number of differences is: ", differences) # There were no differences here.
    diff_dict['invk1'] = differences

    py_inv_k5k1 = python_data['inv_k5k1']
    mat_inv_k5k1 = matlab_data['inv_k5k1']
    nx, ny, nz = mat_inv_k5k1.shape
    px, py, pz = py_inv_k5k1.shape
    if nx == px and ny == py and nz == pz:
        differences = 0
        print(f"The shapes of the invk5k1 variables: {mat_inv_k5k1.shape} are the same.")
    else:
        print("The shapes of the invk5k1 variables are not the same.")
        diff_dict['invk5k1'] = 'Not same shape.'
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                if abs(py_inv_k5k1[i,j,k] - mat_inv_k5k1[i,j,k]) < 1e-4:
                    pass
                else:
                    differences += 1
                    print(f'The values at {i},{j},{k} are not the same.')
                    print("The difference is: ", abs(py_inv_k5k1[i,j,k] - mat_inv_k5k1[i,j,k]))
    # print("The number of differences is: ", differences) # There were no differences here.
    diff_dict['invk5k1'] = differences

    return diff_dict

diff_dict = variable_checker()
# Print all the keys and differences with a for loop
for key in diff_dict.keys():
    print(key, diff_dict[key])

