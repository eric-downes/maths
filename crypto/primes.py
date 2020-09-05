from multiprocessing.sharedctypes import SynchronizedArray
import multiprocessing as mp
from functools import partial
from bitarray import bitarray
from typing import *
import pickle
import ctypes
import arrow
import sys

ShBitArray = Union[bitarray, SynchronizedArray]

def in_ipython() -> bool:
    try: return __IPYTHON__
    except NameError: return False

def default_sieve(stop:int):
    b = bitarray('1') * stop
    b[:2] = False
    return b

def nth_prime_bound(n:int) -> int:
    return math.ceil(n * math.log(n * math.log(n)))

def eratosthenes(n:int) -> list:
    primes = []
    stop = nth_prime_bound(n)
    sieve = default_sieve(stop)
    for i in range(2, stop):
        if sieve[i]:
            primes.append(i)
            for j in range(i * i, stop, i):
                sieve[j] = False
    return primes

def erat_sieve(rng:range, sieve:ShBitArray) -> bitarray:
    # assumes all primes < rng[0] processed into sieve
    l = len(sieve)
    for i in rng:
        if sieve[i]:
            for j in range(i * i, l, i):
                sieve[j] = False
    return sieve

# if we know all primes < n, then we can detect all primes in [n, n*2] async
def range_producer(start:int, ncpus:int = mp.cpu_count()):
    stop = start * 2
    delta = (stop - start) // ncpus
    while start < stop:
        yield range(start, min(stop, start + delta))
        start += delta

if __name__ == '__main__' and not in_ipython():
    print(arrow.now(), f'starting; will calculate first 100M primes')
    n = nth_prime_bound(10 ** 8)
    i = 2 ** 22
    sieve = erat_sieve(range(2, i), default_sieve(n))
    # mp.Array makes a threadsafe shared mem interface for sieve
    with mp.Pool() as p, mp.Array(ctypes.c_bool, sieve) as b:
        while i < n:
            fcn = partial(erat_sieve, b)
            p.map(fcn, range_producer(i))
            i *= 2
    with open('primes.pkl', 'wb') as f:
        pickle.dump(sieve, f)
    print(arrow.now(), f'finished; prime sieve in primes.pkl')
    
