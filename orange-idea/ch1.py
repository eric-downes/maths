'''
can we go from the N-ary relations bigraph to the Formal Concepts bigraph in TDBs work?

for finding could try this:
https://stackoverflow.com/questions/1348783/finding-all-disconnected-subgraphs-in-a-graph

can use multiprocessing to split the problem
0. sparse rep -> list of nodes
1. each worker takes a piece of the graph
2. each worker assigns label & publishes, then:
3. gets next nodes & assigns labels there & publishes
4. if we have a globally readable dict can do O(1) lookup
   --> as soon as a node finds one of its labels intersect w/ another,
       publishes this collisin to a process that notifies the appropriate children
       they merge their data and one of the processes ends
5. continue until all node in 0 have been assigned and then wait for chldren to finish
(can we use this with time-frames to split blockchain interactions into seperate problems?)
   --> what would a db look like?  f(start, end, node) = [ connected-nodes ]
       could use bloom filters to store... if we did that how do we sanity-check the returned?
''' 

from collections import defaultdict
from functools import reduce
from typing import *
import warnings

# this is TDB's system w/ same syntax
# if we inherit from nx.DiGraph can -> graph & use connected_components to find formal concepts
# https://networkx.github.io/documentation/networkx-1.9.1/reference/generated/networkx.algorithms.components.connected.connected_components.html

# these involve fixed points... so does Jost CM Ch 2's general diagonalization argument ... related?
# IF SO then we can prove fixed points exist by detecting the surjectivity of a function...

class PreConcept:
    def __init__(self, rels: Set[Tuple[Any, Any]]):
        X = set()
        Y = set()
        a = defaultdict(lambda : set())
        b = defaultdict(lambda : set())
        for l, r in rels:
            a[l].add(r)
            b[r].add(l)
        self.a = a
        self.b = b
        self.X = X
        self.Y = Y
    def ext(self, sub:set, to_right:bool = True) -> set:
        home = a if to_right else b
        assert(sub.issubset(home.keys()))
        return set.intersection( *{home[x] for x in sub} )
    def f(self, A:set) -> set:
        return self.ext(A)
    def g(self, B:set) -> set:
        return self.ext(B, False)
    def formal_concepts(self):
        fc = set()
        for A in powerlist(a.keys()):
            B = f(A)
            if not B: continue
            if A == g(B): fc.add({A,B})
        return fc

class NDRelation: #my n-dim extension
    def __init__(self, rels:Iterable[set]):
        objs = set()
        emaps = defaultdict(set)
        dmaps = defaultdict(set)
        imaps = dict() #{id(None): set()} # used in .image() below
        for s in map(frozenset, rels):
            d = len(s)
            if d <= 1: continue
            sid = id(s)
            imaps[sid] = s
            objs.update(s)
            for e in s:
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
        return {self._imaps[sid] - rm for sid in self._emaps[e]}
        
    def fiber(self, e, U:bool = True, rm_self:bool = True):
        f = frozenset.union if U else frozenset.intersection
        rm = {e} if rm_self else set()
        return f( *self.images(e, rm_self=False) ) - rm

    def preimage(self, sub:set, U:bool = True, rm_self:bool = True): 
        sub = sub.intersection(self.objects) # otherwise if U risk false {} preimage
        f = frozenset.union if U else frozenset.intersection
        rm = sub if rm_self else set()
        return f( *{self.fiber(e, U, False) for e in sub} ) - rm

    # TDB's "extension f(A) of a(x)" is preimage(A, U = False)
    def extension(self, sub:set, rm_self:bool = True): 
        return self.preimage(sub, U=False, rm_self = rm_self)

    def relations(self):
        return self._imaps.values()

    def export_as(self, typ):
        if typ == pd.DataFrame: pass # export table / biadjacency matrix
        if typ == nx.Graph: pass # export hypergraph as bigraph

    @classmethod
    def test_self():
        R = {frozenset(s) for s in [{1,2}, {1,2,3}, {1,3}, {3,4}]}
        ndrel = NDRelation(R)
        assert ndrel.objects == {1,2,3,4}, "objects"
        assert ndrel.images(1) == {frozenset(s) for s in [{2},{2,3},{3}]}, "images"
        assert ndrel.fiber(1) == {2,3}, "fiber"
        assert ndrel.preimage({3,4}) == {1,2}, "preimage"
        assert ndrel.extension({2,3}) == set(), "empty extension"
        assert ndrel.extension({2}) == {1}, "non-empty ext"

        R = {frozenset(s) for s in [{'orange','fruit'},
                                    {'green','fruit'},
                                    {'purple','vegetable'}]}
        ndrel = NDRelation(R)
        assert ndrel.images('orange') == {frozenset({'fruit'})}
        assert ndrel.images('fruit') == {frozenset(s) for s in [{'orange'}, {'green'}]}
        assert ndrel.extension({'orange','green'}) == {'fruit'}
        assert ndrel.extension({'purple'}) == {'vegetable'}
        assert ndrel.extension({'orange','purple'}) == set()

        
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

def ndrel_to_preconcept()
            
            
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
