from tqdm import tqdm
import numpy as np
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