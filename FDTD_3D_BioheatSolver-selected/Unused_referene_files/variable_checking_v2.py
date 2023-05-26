# This python file will be used to check differences between variables in the matlab code and the python code.

import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt

matlab_data = sio.loadmat('variables_to_check.mat')
print(matlab_data.keys())
python_data = sio.loadmat('py_vars_to_check.mat')
print(python_data.keys())
diff_dict = {}

def variable_checker(var1, var2, key_name):
    # This function will check the variables in the matlab code and the python code.
    # The variables should be similar within a tolerance of 1e-6
    # We return a dictionary of the names of the variables and the number of differences.
    # The variables to check are:
    # Temps, inv_k1, invk5k1, rho_cp, k1, and k8
    # load all the variables from each file
    diff_value = 1e-6
    #now compare the two variables with a for loop and a tolerance of 1e-6
    size_tuple = var1.shape
    size_tuple2 = var2.shape
    if size_tuple == size_tuple2:
        differences = 0
        print(f'The shapes of the {key_name} variables: {var1.shape} are the same.')
        #reshape both arrays to 1D arrays
        var1 = var1.reshape(-1)
        var2 = var2.reshape(-1)
        m = iter(var1)
        p = iter(var2)
        while(True):
            try:
                m_next = next(m)
                p_next = next(p)
                if abs(m_next - p_next) < diff_value:
                    pass
                else:
                    differences += 1
                    # print(f'The values at {m_next} are not the same.')
                    # print("The difference is: ", abs(m_next - p_next))
            except StopIteration:
                break
    else:
        print(f'The shapes of the {key_name} variables are not the same.')
        print(f'The shape of the matlab variable is: {size_tuple}')
        print(f'The shape of the python variable is: {size_tuple2}')
        return 'Not same shape.'
    #depending on the length of the size tuple, we need to use a different for loop.

    print("The number of differences is: ", differences) # the number of differences here was 5398548. That's way too many.

    return differences

for key in matlab_data.keys():
    intro_keys = ['__header__', '__version__', '__globals__']
    # Take the key and find the same key in the python data starting at key 3.
    # Then run the function to compare the two variables
    # Then add the key and the number of differences to the dictionary
    if key not in intro_keys:
        if key in python_data.keys():
            differences = variable_checker(matlab_data[key], python_data[key], key)
            diff_dict[key] = differences
        else:
            print(f'The key {key} is not in the python data.')
            diff_dict[key] = 'Not in python data.'

# Print all the keys and differences with a for loop
for key in diff_dict.keys():
    print(key, diff_dict[key])

