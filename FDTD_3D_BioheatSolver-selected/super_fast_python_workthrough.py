# example of loading matrices and multiplying them together (optimal numpy threads)
from os import environ
# set threads equal to number of physical cores (with openblas)
environ['OMP_NUM_THREADS'] = '6'
from numpy.random import rand
from time import time
 
# function for creating a test matrix
def load_data(n=500):
    # square matrix of random floats
    return rand(n, n)
 
# function for performing operation on matrices
def operation(item1, item2):
    # matrix multiplication
    return item1.dot(item2)
 
# record the start time
start = time()
# load data
data1 = [load_data() for _ in range(100)]
data2 = [load_data() for _ in range(100)]
# apply operation to items
results = [operation(item1, item2) for item1,item2 in zip(data1,data2)]
# calculate and report duration
duration = time() - start
print(f'Took {duration:.3f} seconds')