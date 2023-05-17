# Numpy arrays are mutable. If you want to make a copy of a numpy array, you need to use the copy() method.
# All elements of a numpy array must be of the same type. If you try to create a numpy array with different types, 
# numpy will upcast if possible. For example, if you try to create an array with an integer and a float, numpy will upcast the integer to a float.

# There are many different ways to create numpy arrays. Here are some examples:
# Array(): create an array from a lists or tuples
import numpy as np
a = np.array([1,2,3,4,5])
b = np.array([[1,2,3],[4,5,6]]) # 2D array
c = np.array([1,2,3,4,5], dtype='float32') # specify data type
c2 = np.array([1,2,3,4,5], dtype="complex") # makes the array have complex numbers
d = np.array([range(i,i+3) for i in [2,4,6]]) # create a 2D array from a list comprehension

g = np.array([[1,1,1],[1,1,1]])
print(g.shape)
h = np.array([[1,2],[3,4],[5,6]])
print(h.shape)
gh = np.matmul(g,h) # matrix multiplication needs array of shape (n,m) and (m,p) to get array of shape (n,p)
print(f"matmul, gh: \n{gh}")
gh2 = np.dot(g,h) # dot product
print(f"dot product, gh2: \n{gh2}")
gh3 = g * h # element-wise multiplication needs array of same shape.
print(f"element-wise multiplication, gh3: \n{gh3}")


print(f"c2: {c2}")
"""
array(...)
    array(object, dtype=None, *, copy=True, order='K', subok=False, ndmin=0,
          like=None)
    
    Create an array.
    
    Parameters
    ----------
    object : array_like
        An array, any object exposing the array interface, an object whose
        __array__ method returns an array, or any (nested) sequence.
        If object is a scalar, a 0-dimensional array containing object is
        returned.
    dtype : data-type, optional
        The desired data-type for the array.  If not given, then the type will
        be determined as the minimum type required to hold the objects in the
        sequence.
    copy : bool, optional
        If true (default), then the object is copied.  Otherwise, a copy will
        only be made if __array__ returns a copy, if obj is a nested sequence,
        or if a copy is needed to satisfy any of the other requirements
        (`dtype`, `order`, etc.).
    order : {'K', 'A', 'C', 'F'}, optional
        Specify the memory layout of the array. If object is not an array, the
        newly created array will be in C order (row major) unless 'F' is
        specified, in which case it will be in Fortran order (column major).
        If object is an array the following holds.
    
        ===== ========= ===================================================
        order  no copy                     copy=True
        ===== ========= ===================================================
        'K'   unchanged F & C order preserved, otherwise most similar order
        'A'   unchanged F order if input is F and not C, otherwise C order
        'C'   C order   C order
        'F'   F order   F order
        ===== ========= ===================================================

        When ``copy=False`` and a copy is made for other reasons, the result is
"""
# arange(): 
# basically this means: create an array with all the numbers from a start and stop value. 
"""values are generated within the half open interval ''[start, stop]''
    one of the optional arguments for the function is a step size, however, the docs say
    to avoid using non-integer step sizes.  """
# linspace()
"""creates a number of evenly spaced values between start and end points specified. 
    Start is optional, default 0, with specified ending. 
    You can also specify the number of values you wished, and whether to include 
    the ending value or n+1. You can also print the step size if you wish.
    also, can specify data type through dtype="___"
    retstep=True returns the samples and the step size used to create them. """
# zeros()
""" syntax: zeros(shape, dtype=float, order='C', *, like=None)
    shape: int or tuple of ints, you can also put in a list with two ints.
    side note: like : array_like, optional
            Reference object to allow the creation of arrays which are not
            NumPy arrays. If an array-like passed in as ``like`` supports
            the ``__array_function__`` protocol, the result will be defined
            by it. In this case, it ensures the creation of an array object
            compatible with that passed in via this argument.
"""
# ones()
""" Very similar to zeros, pretty much the same syntax. """
# eye()
""" This is the function that will return an ndarray with diagonal 1s. 
    eye(N, M=None, k=0, dtype=<class 'float'>, order='C', *, like=None)
    N is number of rows, M columns, k=0 is which diagonal to put the ones. 
    Positive (+) is upper diagonal. 
    negative (-) is lower diagonal.
    for greater positive or negative values, the diagonal will be futher away from the main diagonal. 
    Similar functions:
    identity() almost equivalent function, but with less functionality. It only takes N and dtype as arguments.
    diag() diagonal 2-D array from a 1-D array specified by the user.
"""
# random()
"""
    rand() creates an array of the given shape and populates it with random samples from a uniform distribution over [0, 1).
        examples: >>> np.random.rand(5) # 1D array with 5 random numbers.
    randn() creates an array of the given shape and populates it with random samples from a standard normal distribution centered on 0.
    randf() creates an array of the given shape and populates it with random floats over [0, 1).
    randint() creates an array of the given shape and populates it with random integers from low (inclusive) to high (exclusive).
    random() creates an array of the given shape and populates it with random samples from a uniform distribution over [0, 1).
"""

# Array attributes
"""
    ndim: the number of dimensions of the array
    shape: the size of each dimension returned as a tuple
    size: the total size of the array aka the total number of elements in the array.
    dtype: the data type of the array
    itemsize: the size (in bytes) of each array element (64 bits = 8 bytes, 8 bits = 1 byte)
    nbytes: the total size (in bytes) of the array 
"""
# Array indexing
"""
    array indexing is very similar to list indexing.
    can retrieve a single element by indexing with square brackets
        Uses Zero-based indexing
        Can use negative indices to index from the end of the array (e.g. -1 is the last element, 
        -2 is the second to last element and so on.)
        Can use a tuple of indices to index multidimensional arrays
    array slicing is also very similar to list slicing
        syntax of slicing: array[start:stop:step, start:stop:step, etc.] start is inclusive, stop is exclusive
        Uses Zero-based indexing
        Uses the colon operator (:) to specify the start and end of the slice
"""
# Array Arithmetic Operations
"""
    Arithmetic operators on arrays apply elementwise. A new array is created and filled with the result.
    Arithmetic operations on arrays are usually done on corresponding elements. If two arrays are of the 
    same shape, then these operations are done on an element-by-element basis.


"""
