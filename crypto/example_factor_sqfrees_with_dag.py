from typing import *
import numpy as np
import ray

from generic import *

#ray.init(ignore_reinit_error=True)

Fan = Dict[int, Set[int]]

def sort_into(val, arr:list, key:Callable = lambda x:x[0]) -> list:
    if not arr: return [val]
    i = lub_index(val, arr, key)
    return arr[:i] + [val] + arr[i:]

def dag_gen(primes:Set[int], stop_above:int) -> Fan:
    dag = {}
    delta = {}
    for p in primes:
        delta[p] = {x * p for x in primes - {p}}
    while delta:
x        dag.update(delta)
        delta = {}
        for vs in dag.values():
            for v in vs - dag.keys():
                if v <= stop_above:
                    delta[v] = {v * p for p in primes if v % p}
                else:
                    delta[v] = set()
    return dag

def factor(sqfrees:Set[int], primes:Set[int]) -> Tuple[Fan, Set[int]]:
    solns = {}
    stop_above = max(sqfrees)
    print('starting')
    dag = dag_gen(primes, stop_above)
    print('calculated dag')
    paths = [(p, {p}) for p in primes]
    while sqfrees and paths:
        k, factors = paths.pop()
        for n in dag[k]:
            if n > stop_above:
                continue
            if n in sqfrees:
                sqfrees.discard(n)
                solns[n] = factors|{n // k}
            else:
                paths = sort_into((n, factors|{n // k}), paths)
    return solns, sqfrees

def test_integration():
    primes = {2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,51,53,57}
    sqfree = {2*3*57: {2,3,57},
              5*7*53: {5,7,53},
              11*13*17*51: {11,13,17,51},
              19*23*29*47: {19,23,29,47},
              31*37*41*43: {31,37,41,43}}
    assert (sqfree, set()) == (factor(set(sqfree.keys()), primes))
    
if __name__ == '__main__':
    test_integration()
    
