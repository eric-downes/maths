from collections import defaultdict
from functools import reduce
from typing import *
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
        self._emaps = emaps # object -> set of sid's
        self._dmaps = dmaps # rank -> set of sid's
        self._imaps = imaps # sid -> set of objects
        
    # TDB is using set-valued functions so ea image is also a set
    # each element of these is the image of a morphism in Set
    def images(self, e, rm_self:bool = True):
        rm = {e} if rm_self else set()
        return {s - rm for sid in self._emaps[e] for s in self._imaps[sid]}
        
    def fiber(self, e, U:bool = True, rm_self:bool = True):
        f = set.union if U else set.intersection
        rm = {e} if rm_self else set()
        return f( *self.images(e, rm_self=False) ) - rm

    def preimage(self, sub:set, U:bool = True, rm_self:bool = True): 
        sub = sub.intersection(self.objects) # otherwise if U risk false {} preimage
        f = set.union if U else set.intersection
        rm = sub if rm_self else set()
        return f( *{self.fiber(e, U, False) for e in sub} ) - rm

    # TDB's "extension f(A) of a(x)" is preimage(A, U = False)
    def extension(self, sub:set, rm_self:bool = True): 
        return self.preimage(sub, U=False, rm_self)

    def relations(self):
        return self._imaps.values()

    def table(self):
        pass
    
    def test_self(full = False):
        R = {{1,2}, {1,2,3}, {1,3}, {3,4}}
        ndrel = NDRelation(R)
        assert(ndrel.objects == {1,2,3,4})
        assert(ndrel.images(1) == {{2}, {2,3}, {3}})
        assert(ndrel.fiber(1) == {2,3})
        assert(ndrel.preimage({3,4}) == {2,3,4})
        assert(ndrel.extension({2,3}) == set())
        assert(ndrel.extension({2}) == {1})

        R = {{'orange','fruit'}, {'green','fruit'}, {'purple','vegetable'}}
        ndrel = NDRelation(R)
        assert(ndrel.images('fruit') == {{'orange'}, {'green'}})
        assert(ndrel.extension({'orange','green'}) == {'fruit'})
        assert(ndrel.extension({'purple'}) == {'vegetable'})

        
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
        for sub in powerlist(seq[1:]):
            yield [seq[0]] + sub
            yield sub

def concept_generator(self, seq=list(self.objects)):
    if len(seq) > 1:
        for sub in concept_search(seq[1:]):
            x = [seq[0]] + sub
            if self.extension(set(x))
            yield [seq[0]] + sub
            yield sub

            
'''
0. test what we have so far
1. we are implementing a hypergraph here...
any hypergraph can be represented as a bipartite graph
so we should make those concepts explicit & accessible

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
