# My notes on parallelism in Python, Specifically on speeding up Calc_TEMPS_v04S_python.py

## Threads vs Processes
    Python by default uses only one thread and one process at one time. 
    This is because of the Global Interpreter Lock (GIL) which prevents multiple threads from executing Python bytecodes at once.
    
## However, Numpy and Scipy Bypass the GIL
    Numpy and Scipy are written in C and Fortran, and bypass the GIL by releasing it when doing computationally intensive tasks.
    This means that Numpy and Scipy can use multiple threads and processes to speed up their computations.
    
    In the Calc_TEMPS_v04S_python.py file, the computationally intensive tasks are the for loops that calculate the temperature
    Throughout the execution of the for loop iterations, most of the computationally intensive tasks are array additions and
    element by element multiplications. These are tasks that Numpy and Scipy can do in parallel by default. 
    (Assuming you have the BLAS and LAPACK libraries installed.) (https://superfastpython.com/what-is-blas-and-lapack-in-numpy/ , https://superfastpython.com/numpy-vs-gil/) 
    This means that the program is already running in parallel, and would recieve little to no benefit from using the multiprocessing.

