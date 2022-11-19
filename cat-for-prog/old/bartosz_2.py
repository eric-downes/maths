# https://bartoszmilewski.com/2014/12/05/categories-great-and-small/

'''
instead of storing objects in a set, we'll store them internally in a
list.  the list is a topological sort of the objects using the
preorder inherited from it's morphisms
'''

import functools as ft
import graphviz as gv
import networkx as nx
from typing import *

def rand_like(t: Union[type,Any]): pass

class Monoid:
    def __init__(self, mempty: Any, mappend: Callable[[Any, Any], Any]):
        assert(mempty == mappend(mempty, mempty)) # identity
        x = rand_like(mempty)
        assert(x == mappend(x, mempty))
        assert(x == mappend(mempty, x))
        y = rand_like(mempty)
        z = rand_like(mempty)
        assert(mappend(mappend(x, y), z) == mappend(x, mappend(y, z)))
        self.binop = mappend
        self.unit = mempty

class Morphism:
    def __init__(self, domain:Any, codomain:Any, fcn:Callable):        
        self.dom = domain
        self.codom = codomain
        self.map = fcn
    def __call__(self, *args, **kwargs):
        return self.map(*args, **kwargs)
        
class FinCat:
    
    def __init__(self):
        self._topsort = list()
        self._imaps = dict()
        self._domaps = dict()
        self._comaps = dict()
        self._graph = nx.DiGraph()

    def objects(self):
        return set(self._topsort)

    def bottom(self): # may not be unique, but will be <= all objs
        return self._topsort[0] if len(self._topsort) else None

    def homset(self):
        return set(self._imaps.values())
    
    def free_closure(self):
        # need bottom element + topological sort to make efficient....
        pass 
        
    def add_objects(self, objects:set,
                    inplace:bool = False,
                    free:bool = True):
        new = self
        new.objects |= objects
        new._graph.add_nodes_from(objects)
        if free: new.free_closure()
        if not inplace: return new
        self = new
        
    def add_morphs(self, morphs: List[Morphism],
                   inplace:bool = False,
                   free:bool = True):                   
        miss = set()
        edges = []
        imaps = self._imaps
        domaps = defaultdict(set, self._domaps)
        comaps = defaultdict(set, self._comaps)
        graph = self._graph
        for f in morphs:
            i = id(f)
            if i in imaps: continue
            imaps[i] = f
            domaps[f.dom] |= {i}
            comaps[f.codom] |= {i} 
            miss |= {f.dom, f.codom}
            graph.add_edge(f.dom, f.codom, label=i)
        new = FinCat()
        new.objects = self.objects | miss
        new._imaps = imaps
        new._comaps = dict(comaps)
        new._domaps = dict(domaps)
        new._graph = graph
        if free: new.free_closure()
        if not inplace: return new
        self = new

    
