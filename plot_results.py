import numpy as np
import matplotlib.pyplot as plt

x, y, z, w = np.loadtxt('results_nogil.dat', delimiter='\t', unpack=True)

plt.plot(x, y, 'r.-', label = 'numba function')
plt.plot(x, z, 'b.-', label = 'python function')
plt.plot(x, w, 'g.-', label = 'ctype function')
plt.ylabel('time (s)')
plt.xlabel('n iterations')
plt.yscale('log')
plt.xscale('log')
plt.legend(loc='lower right')
plt.grid(True)
plt.title('pi computation')
plt.savefig("compute_pi_serial_benchmark_nogil.png")
#plt.show()
