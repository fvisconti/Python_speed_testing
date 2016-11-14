import ctypes
import time

# import the C library
mylib = ctypes.CDLL('pi_c.so')
# declare result type: default is int
mylib.compPi_ctypes.restype = ctypes.c_double
# declare arguments type
pi = ctypes.c_double(0.); niter = ctypes.c_int(1000)

start = time.clock()
pictversion = mylib.compPi_ctypes(pi, niter)
stop = time.clock()
c_time = stop - start

print("time for c version: {}".format(c_time))
