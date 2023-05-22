# This python file will be used to check differences between variables in the matlab code and the python code.

import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt

matlab_data = sio.loadmat('variables_to_check.mat')
print(matlab_data.keys())
python_data = sio.loadmat('py_vars_to_check.mat')
print(python_data.keys())
diff_dict = {}

def variable_checker(var1, var2):
    # This function will check the variables in the matlab code and the python code.
    # The variables should be similar within a tolerance of 1e-6
    # We return a dictionary of the names of the variables and the number of differences.
    # The variables to check are:
    # Temps, inv_k1, invk5k1, rho_cp, k1, and k8
    # load all the variables from each file
    
    #now compare the two variables with a for loop and a tolerance of 1e-6
    nx, ny, nz, nt  = var1.shape
    px, py, pz, pt = var2.shape
    if nx == px and ny == py and nz == pz and nt == pt:
        differences = 0
        print("The sizes of the temps variables are the same.")
    else:
        print("The sizes of the temps variables are not the same.")
        return 'Not same shape.'
    if nt >=2:
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    for l in range(nt):
                        if abs(var2[i,j,k,l] - var1[i,j,k,l]) < 1e-4:
                            pass
                        else:
                            differences +=1
    else:
        # This means we need to use a 3D for loop to iterate over the variables.
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    if abs(var2[i,j,k] - var1[i,j,k]) < 1e-4:
                        pass
                    else:
                        differences += 1
    print("The number of differences is: ", differences) # the number of differences here was 5398548. That's way too many.

    return differences

for key in matlab_data.keys():
    # Take the key and find the same key in the python data
    # Then run the function to compare the two variables
    # Then add the key and the number of differences to the dictionary
    if key in python_data.keys():
        differences = variable_checker(matlab_data[key], python_data[key])
        diff_dict[key] = differences
    else:
        print(f'The key {key} is not in the python data.')
        diff_dict[key] = 'Not in python data.'

# Print all the keys and differences with a for loop
for key in diff_dict.keys():
    print(key, diff_dict[key])

