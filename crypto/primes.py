'''
inefficient primes... try using seive of erastothenes
'''
from functools import partial, reduce
import multiprocessing as mp
from operator import and_
from typing import *
import pickle
import arrow
import sys

def in_ipython():
    try: return __IPYTHON__
    except NameError: return False

# mp doesnt offer a shared set, so we use a list
def relative_primes(r:range, primes:list = None):    
    if not primes: primes = [r[0]]
    l = len(primes)
    for i in r[1:]:
        if i == 1: continue
        if reduce(and_, [bool(i % j) for j in primes], True):
            primes.append(i)
    return primes

# if we know all primes < n, then we can detect all primes in [n, n*2] async
def range_producer(start:int, ncpus:int = mp.cpu_count()):
    stop = start * 2
    delta = (stop - start) // ncpus
    while start < stop:
        yield range(start, start + delta)
        start += delta

def test():
    assert [2,3,5,7] == relative_primes(range(2,10), [])
        
if __name__ == '__main__' and not in_ipython():
    print(arrow.now(), f'starting')
    n = int(sys.argv[1])
    top = int(sys.argv[2])
    with mp.Pool() as p, mp.Manager() as m:
        shared_primes = m.list(relative_primes(range(2,n)))
        while n < top:
            f = partial(relative_primes, primes = shared_primes)
            p.map(f, range_producer(n))
            print(arrow.now(), f'finished n={n}; {len(shared_primes)} found')
            n *= 2
        pickle.dump(shared_primes, open('primes.pkl','wb'))
        
