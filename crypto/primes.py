from multiprocessing.sharedctypes import SynchronizedArray
import multiprocessing as mp

from sympy.ntheory.factor_ import primenu
from functools import partial
from bitarray import bitarray
from typing import *
import pickle
import ctypes
import arrow
import math
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

def _factor_hlpr(n:int, k:int, factors:set) -> Set[Tuple[int,int]]:
    w = 0
    while n % k: # optimized for square-free
        n = n // k
        w += 1
    if w: factors.add((k, w))
    return factors

# NEEDS TESTING
def factor(n:int) -> Set[Tuple[int,int]]:
    pfactors = set()
    _factor_hlpr(n, 2, pfactors)    
    for k in range(3, int(n ** (1/2)) + 1, 2):
        _factor_hlpr(n, k, pfactors)
    if n > 2: pfactors.add( (n, 1) )
    return pfactors

# NEEDS TESTING
def _omega_hlpr(factors:Set[Tuple[int,int]]) -> Tuple[int,int]:
    omega = len(factors)
    Omega = sum(map(lambda t: t[1], factors))
    mu = 0 if Omega > omega else (-1 if omega % 2 else 1)
    return (facprint(factors), mu, omega, Omega, omega + Omega)

# broken?
# demo only; use euclid for prod
def gcd_omegas(i:int, j:int):
    sm, big = (i, j) if i <= j else (j, i)
    df = pd.DataFrame(index=['u','o','O','oO'])
    row = _omega_hlpr(factor(big))
    df[row[0]] = row[1:]
    while sm:
        big, sm = (sm, big % sm)
        row = _omega_hlpr(factor(big))
        df[row[0]] = row[1:]
        print(big, sm, *dot[big])
    return big, df.T
        
# fastest if you can mp
def factor_with_primes(n:int, primes:list, check:bool = True) -> Tuple[Set[Tuple[int,int]], int]:
    fcn = partial(_factor_hlpr, n = n, pfactors = set())
    with mp.Pool() as p:
        los = p.map(fcn, primes)
    pfactors = set.union(los)
    # can skip these steps using mp.Value?
    if check:
        reached = reduce(operator.mul, map(lambda t: t[0] ** t[1], pfactors))
        assert 0 == n % reached, "abandon ship; math is broken!"
        k = n // reached
    else: k = 0
    return pfactors, k


# if you already have a sieve
# adapt this to also work with dict sieve
def factor_with_sieve(n:int, sieve:ShBitArray) -> Tuple[Set[Tuple[int,int]], int]:
    reach = len(sieve)
    pfactors = set()
    _factor_hlpr(n, 2, pfactors)
    sqrtn = int(n ** (1/2)) + 1
    in_reach = sqrtn < reach
    top = sqrtn if in_reach else reach
    for k in range(3, top, 2):
        if sieve[k]: _factor_hlpr(n, k, pfactors)
        if n < reach and sieve[n]:
            pfactors.add( (n, 1) )
            n = 1
            break
    if n > 2 and in_reach: pfactors.add( (n, 1) )
    return pfactors, n

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

def first_n_primes(n:int) -> List[int]:
    primes = pickle.load(open('primes.pkl','rb'))
    if len(primes) >= n: return primes[:n]
    raise NotImplementedError(f'retrieval > {n} not implemented yet ... adapt __main__ clause?')

def euclid(i:int, j:int):
    sm, big = (i, j) if i <= j else (j, i)
    while sm: big, sm = (sm, big % sm)        
    return big


if __name__ == '__main__' and not in_ipython():
    # 19 min 54 sec for 100M primes serial version
    print(arrow.now(), f'starting; will calculate first 100M primes')
    n = nth_prime_bound(10 ** 8)
    i = 2 ** 12
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
    
