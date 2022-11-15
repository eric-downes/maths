from __future__ import annotations
from hashlib import blake2b
from typing import *

import numpy as np

PreEndo = int|list[int]

class Endo(list):
    def __init__(self, l:PreEndo):
        if isinstance(l, int):
            l = [l]
        super().__init__(l)
        self.is_id = self == list(range(len(self)))
    def __mul__(self, other:PreEndo|Endo) -> Endo:
        return self(other)
    def __rmul__(self, other:PreEndo|Endo) -> Endo:
        if not isinstance(other, Endo):
            other = Endo(other)
        return other(self)
    def __call__(self, other:PreEndo|Endo, strict:bool = True) -> Endo:
        if not isinstance(other, Endo):
            other = Endo(other)
        if strict: assert len(self) == len(other)
        if self.is_id: return other.copy()
        if other.is_id: return self.copy()
        return Endo([self[i % len(self)] for i in other])

class FiniteMonoid(FiniteMagma):
    def __init__(self, lol:list[list[int]]|np.array):
        super().__init__(lol)
        if not self.unital:
            self.order += 1
            self.table[self.order] = np.arange(self.order)
            
        
    
class FiniteMagma:
    def __init__(self, lol:list[list[int]]|np.array):
        self.table = shm_array(lol)
        assert (np.issubdtype(self.table.dtype, np.integer)
                and (0 <= self.table < n).all()), 'not closed as written'
        assert self.table.shape == (n, n), 'not square'
        self.order = len(self.table)
        self.unital = (np.arange(len(lol))) == self.table).all(1).any()
        self.hashes = {the_hash(self.table[i]):i for i in range(self.order)}
        # make table a shared-memory object
        
    def row_monoid(self) -> Monoid:
        # need to detect/adjoin identity as well
        name = shm_copy(self.table) # do the memory thing
        q = mp.Queue()
        search_fcn = ft.partial(new_row, table_name = name, q = q)
        procs = []
        row_monoid = {}
        jn = {'j':0, 'n':self.order}
        hs = self.hashes.copy()
        while outer_loop(name, search_fcn, jn, procs, hs, q, row_monoid):
            if caught_up(jn, q):
                while procs:
                    procs.pop().join()
        return Monoid.from_dok(row_monoid)

class Coset(set):
    def __init__(self, *args, op:Binop = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.op = op
        
    def __mul__(self, x:Any):
        return {self.op(x,y) for y in self}
        
def shm_array(name:str): pass

def shm_resize(name:str): pass

def shm_copy(arr:np.array): pass
    
def caught_up(jn:dict[str, int], q:mp.Queue) -> bool:
    return q.empty() and jn['n'] - 1 == jn['j']

def the_hash(x:np.array) -> bytes:
    return blake2b(x).digest()

def new_row(i:int, j:int, table:np.array, q:mp.Queue) -> None:
    if ((new := table[i][ table[j] ]) != table).any(1).all():
        q.put((i, j, new, the_hash(new)))

def look_for_new_rows(search_fcn:Callable[[int,int],None],
                      jn:dict[str,int],
                      procs:list[mp.Process]) -> None:
    for i in range(jn['n']):
        for j in range(jn['j'], jn['n']):
            p = mp.Process(target = search_fcn, args = (i, j))
            p.start()
            procs.append(p)
    jn['j'] = j

def add_new_rows(name:str,
                 jn:dict[str,int],
                 hashes:dict[bytes,int],
                 q:mp.Queue,
                 row_monoid:dict[tuple[int,int],int]) -> None:
    table = shm_array(name)
    for i, j, new, new_hash in iter(q.get, [None] * 4):
        if i is None: break
        if (k := hashes.get(new_hash, None)) is None:
            jn['n'] += 1
            k = jn['n']
            if k > len(table):
                shm_resize(name)
            table[k] = new
            hashes[new_hash] = k
        row_monoid[(i,j)] = k

def outer_loop(name:str,
               search_fcn:Callable[[int, int], None],
               jn:dict[str, int],
               procs:list[mp.Process],
               hashes:dict[bytes, int],
               q:mp.Queue,
               row_monoid:dict[tuple[int, int], int]) -> bool:
    look_for_new_rows(search_fcn, jn, procs)
    add_new_rows(name, jn, hashes, q, row_monoid)
    return procs or not caught_up(jn, q)
    
