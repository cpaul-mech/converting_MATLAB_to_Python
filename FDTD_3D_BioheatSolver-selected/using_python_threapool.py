# example with threading and no numpy threads
from os import environ
# turn off threads in numpy (with openblas)
environ['OMP_NUM_THREADS'] = '1'
from numpy.random import rand
from multiprocessing.pool import ThreadPool
from time import time
 
# function for creating a test matrix
def load_data(n=500):
    # square matrix of random floats
    return rand(n, n)
 
# function for performing operation on matrices
def operation(item1, item2):
    # matrix multiplication
    return item1.dot(item2)
 
# function that defines a single task
def task():
    # load items
    item1 = load_data()
    item2 = load_data()
    # perform operation
    result = operation(item1, item2)
    return result
 
# record the start time
start = time()
# create thread pool
with ThreadPool(6) as pool:
    # issue tasks and gather results
    results = [pool.apply_async(task) for _ in range(100)]
    # close the thread pool
    pool.close()
    # wait for tasks to complete
    pool.join()
# calculate and report duration
duration = time() - start
print(f'Took {duration:.3f} seconds')