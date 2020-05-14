'''
0. test what we have so far
1. we are implementing a hypergraph here...
any hypergraph can be represented as a bipartite graph
so we should make those concepts explicit & accessible
'''

from collections import defaultdict
from functools import reduce
import warnings

class NDRelation:
    def __init__(self, rels:Set[set]):
        objs = set()
        emaps = defaultdict(set)
        dmaps = defaultdict(set)
        imaps = dict() #{id(None): set()} # used in .image() below
        for s in map(frozenset, rels):
            d = len(s)
            if d <= 1: continue
            sid = id(s)
            imaps[sid] = s
            for e in s:
                objs.add(e)
                emaps[e].add(sid)
                dmaps[d].add(sid)
        self.objects = frozenset(objs)
        self._emaps = emaps
        self._dmaps = dmaps
        self._imaps = imaps

    # TDB is using set-valued functions so ea image is also a point
    def images(e, rm_self:bool = True, check_memb:bool = True):
        if check_memb and e not in self.objects: return set()
        rm = {e} if rm_self else set()
        return {s - rm for sid in self._emaps.get(e, dict()) for s in self._imaps[sid]}
        
    def fiber(e, U:bool = True, rm_self:bool = True, check_memb:bool = True):
        if check_memb and e not in self.objects: return set()
        f = set.union if U else set.intersection
        rm = {e} if rm_self else set()
        return f( *{*self._imaps[sid] for sid in self._emaps[e]} ) - rm

    # TDB's "extension f(A)" is preimage(A, U = False)
    # we remove self at the scale of a fiber
    def preimage(sub:set, U:bool = True, rm_self:bool = True): 
        sub = sub.intersection(self.objects)
        f = set.union if U else set.intersection
        return f( *{self.fiber(e, U, rm_self, False) for e in sub} )

    def test_self(full = False):
        R = {{1,2}, {1,2,3}, {1,3}, {3,4}}
        ndrel = NDRelation(R)
        assert(ndrel.objects == {1,2,3,4})
        assert(ndrel.images(1) == {{2}, {2,3}, {3}})
        assert(ndrel.fiber(1) == {2,3})
        assert(ndrel.preimage({3,4}) == {2,3,4})
        if full:
            old = set()
            for new in map(set, powerlist(list(ndrel.objects))):
                X = old.issubset(ndrel.preimage(new))
                Y = new.issubset(ndrel.preimage(old))
                assert(x == Y)
                old = new
            
# if empty sets commonly result from fiber and preimage with U=False,
# use intersect() instead of set.intersection() for speed improvement
def intersect(*args):
    try: return reduce(cap, args) 
    except: return {}

def cap(x:set, y:Sequence, raize:bool=True):
    x.intersection_update(y) 
    if raize and not x: raise Exception() 
    return x 

def powerlist(seq:list):
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for sub in powerlist(s[1:]):
            yield [seq[0]] + sub
            yield sub
    
'''
los = [*[{1}]*10, {}, *[{1}]*900] 
%timeit set.intersection(*los)
    35.4 µs ± 64.5 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
%timeit intersect(*los)
    6.96 µs ± 17.4 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)

los = [*[{1}]*10**5, {}, *[{1}]*100]
%timeit set.intersection(*los)
    5.01 ms ± 13.9 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
%timeit intersect(*los)
    748 µs ± 879 ns per loop (mean ± std. dev. of 7 runs, 1000 loops each)

BUT....

los = [*[{1}]*10**5]
%timeit set.intersection(*los)
    5.13 ms ± 79.1 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
%timeit intersect(*los)
    22.7 ms ± 1.55 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
'''
