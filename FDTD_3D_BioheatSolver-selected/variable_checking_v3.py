# This python file will be used to check differences between variables in the matlab code and the python code.
from tqdm import tqdm
import scipy.io as sio
import numpy as np


matlab_data = sio.loadmat('variables_to_check.mat')
print('Matlab Data', matlab_data.keys())
python_data = sio.loadmat('py_vars_to_check.mat')
print('python data', python_data.keys())
diff_dict = {}

def variable_checker(var1, var2, key_name):
    # This function will check the variables in the matlab code and the python code.
    # The variables should be similar within a tolerance of 1e-6
    # We return a dictionary of the names of the variables and the number of differences.
    # The variables to check are:
    # Temps, inv_k1, invk5k1, rho_cp, k1, and k8
    # load all the variables from each file
    diff_value = 1e-5
    #now compare the two variables with a for loop and a tolerance of 1e-6
    var1_Shape = var1.shape
    var2_shape = var2.shape
    if var1_Shape == var2_shape:
        differences = 0
        # subtract the two arrays and iterate through the array checking for differences greater than the diff_value
        diff_array = var1 - var2
        diff_array = diff_array.reshape(-1)
        for i in tqdm(range(len(diff_array)), desc=f'Checking {key_name}'):
            if abs(diff_array[i]) < diff_value:
                pass
            else:
                differences += 1
                # print(f'The values at {m_next} are not the same.')
                # print("The difference is: ", abs(m_next - p_next))
    else:
        return ['Not same shape.', f'matlab shape: {var1_Shape}', f'python shape: {var2_shape}']
    
    print("The number of differences is: ", differences) 

    return [f'diff: {differences}', f'shape: {var1_Shape}']

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

