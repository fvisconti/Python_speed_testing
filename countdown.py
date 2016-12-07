import time

def countdown(n):
    while n > 0:
        n -= 1

c = 50000000

start = time.clock()
countdown(c)
stop = time.clock()

print("elapsed time: {}".format(stop - start))