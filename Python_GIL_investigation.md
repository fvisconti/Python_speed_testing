# Python GIL notes
Not any Python implementation uses **GIL**, but *CPython* and *PyPy* do, and these are the most efficient when running a single threaded application.
If somenone wants to:
- use shared memory threading to exploit multiple cores on a single machine
- write their entire application in Python, including CPU bound elements
- use CPython or PyPy as their interpreter

She will face the GIL problem. 
Thus, she will have to:
1. remove the constraint on shared memory. For example using the ```multiprocessing``` module, in standard from Python 2.6 on. Works fine for so called *embarassingly parallel* applications.
2. Use Python as a *glue language*, moving the computational intensive part of the application in external modules. This is the way chosen by **numpy/scipy** community and **Cython** users, and works pretty fine.
3. Use Python implementation that does not rely on GIL (*Jython* and *IronPython* for instance).
4. Use another language.

> "Ok, but still I **want** to use Python **AND** I **want** to write multi-threaded code."
> "Fine, but CPython as well as PyPy core developers still discourage this." practice.

So what?

## Python glue
Multiprocess is not a real alternative to the problem, since it removes the shared memory constraint. Indeed, the main downside of this approach is that the overhead of message serialisation and interprocess communication can significantly increase the response latency and reduce the overall throughput of an application [PyCon 2015]. Whether or not this overhead is considered acceptable in any given application will depend on the relative proportion of time that application ends up spending on interprocess communication overhead versus doing useful work.

So one can seriously consider n. 2 approach, which is also promoted by the community, and widely used for scientific libraries. Probably this approach is best represented by **Cython**, as well as by the use of *Ctypes*.
The idea is: use Python as a *framework* language for your application, and let lower level modules, written and designed to optimise machine resources, do the computation stuff.

A lot of work has been done by developers, with wrappers for famous libraries like *BLAS* or *LAPACK*, and with really performant toolboxes such as already cited *numpy* or *scipy* - not to mention hyper specialised modules like (ehm.. random pick) **astropy** or **gammapy**.
But the real power of this approach is how easy is to write one's own module, or specialised C function, and call it from a Python application.
There's a less mature project named *Numba*, which has adopted a sort of *OpenACC* approach: you keep writing your gorgeous Python functions, then decorate them with a "*JustInTime*" decorator and there you go.

### An example
The following code makes a comparison between execution times for three functions performing the calculus of \pi:
1. a pure Python version;
2. a **Numba** version;
3. a **Ctype** version.

For the **Ctype** version there's the need to write an external function to be compiled in a shared object, then callable from the Python script.

Results are not surprising: from a number of iterations onwards, pure Python version is more than an order of magnitude slower than its corrispondents written with Ctypes or *decorated* with Numba.
Yes, the most interesting part comes with the word *decorated*, since it's clear that a lot less effort is needed to get the same efficiency as Ctype version.

Here's the code:
```Python
from numba import jit, int32, float32
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
```
[Numba lazy jit](https://github.com/fvisconti/Python_speed_testing/blob/master/compute_pi_serial_benchmark_nodeclared.png)

[Numba decorated with nogil, nopython](https://github.com/fvisconti/Python_speed_testing/blob/master/compute_pi_serial_benchmark_nopython.png)

[Numba with nogil and function signature](https://github.com/fvisconti/Python_speed_testing/blob/master/compute_pi_serial_benchmark_declared.png)

# References
- [Efficiently exploiting multiple cores with Python](http://python-notes.curiousefficiency.org/en/latest/python3/multicore_python.html)
- [Python's hardest problem, revisited](https://jeffknupp.com/blog/2013/06/30/pythons-hardest-problem-revisited/)
- [Interesting Python slides on GIL problem](http://www.dabeaz.com/python/UnderstandingGIL.pdf)
- [Python concurrency from the ground up (D. Beazley)](https://youtu.be/MCs5OvhV9S4)

