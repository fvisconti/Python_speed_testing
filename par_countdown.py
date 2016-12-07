from threading import Thread
import time

def countdown(n):
    while n > 0:
        n -= 1

c = 50000000

t1 = Thread(target=countdown, args=(c//2, ))
t2 = Thread(target=countdown, args=(c//2, ))

start = time.clock()
t1.start(); t2.start()
t1.join(); t2.join()
stop = time.clock()

print("elapsed time: {}".format(stop - start))