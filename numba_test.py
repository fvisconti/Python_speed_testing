from numba import jit, vectorize, int32, float32
import ctypes
import numpy as np
import time


# The Python functions to compute pi:
def f(x):
    return 4. / (1. + x * x)


def compPi(niter=10000000):
    h = 1. / niter
    pi = 0.
    for i in range(niter):
        x = h * (i - 0.5)
        pi += f(x)
    error = abs(np.arccos(-1.) - pi * h) / np.arccos(-1.)
    return pi * h, error


# The Just-In-Time-compiled version:
@jit(float32(float32), nogil=True)
def f_numba(x):
    return 4. / (1. + x * x)


@jit(float32(int32), nogil=True)
def compPi_numba(niter):
    h = 1. / niter
    pi = 0.
    for i in range(niter):
        x = h * (i - 0.5)
        pi += f_numba(x)
    error = abs(np.arccos(-1.) - pi * h) / np.arccos(-1.)
    return pi * h, error


def main():
    # import the C library
    mylib = ctypes.CDLL('pi_c.so')
    # declare result type: default is int
    mylib.compPi_ctypes.restype = ctypes.c_double
    # declare arguments type
    pi = ctypes.c_double(0.)
    # niter = ctypes.c_int(1000)

    numIter = [1000, 10000, 100000, 1000000, 10000000]

    for i in numIter:
        # Numba
        start = time.clock()
        compPi_numba(i)
        stop = time.clock()
        numba_time = stop - start
        print("numba function takes: {}".format(numba_time))

        # Ctype
        niter = ctypes.c_int(i)
        start = time.clock()
        mylib.compPi_ctypes(pi, niter)
        stop = time.clock()
        c_time = stop - start
        print("time for c version: {}".format(c_time))

        # Pure Python
        start = time.clock()
        compPi(i)
        stop = time.clock()
        nonumba_time = stop - start
        print("Pure Python function takes: {}".format(nonumba_time))

        with open('results_nogil.dat', 'a') as file:
            file.write(str(i) + "\t" + str(numba_time) +
                       "\t" + str(nonumba_time) +
                       "\t" + str(c_time) + "\n")


if __name__ == '__main__':
    main()
