from typing import *
import operator as op
from itertools import permutations

import numpy
import numba
import pandas as pd

Num = float|int

@numba.jit
def extrema(a:np.array) ->  tuple[Any,Any]:
    minimum = a[0]
    maximum = a[0]
    for e in a[1:]:
        if e < minimum: minimum = e
        elif e > maximum: maximum = e
    return (minimum, maximum)



class FinBinOp(np.array):
    def __init__(self, table:np.array, strict:bool = True):
        assert len(sh := table.shape) == 2 and sh[0] == sh[1]
        self.table = table
        self._id = blake2b(self.table).digest()
    def is_closed(self) -> bool:
        return self.table.dtype == int and extrema(self.table[:]) in Interval(0, len(self.table), parens = '[)')
    def is_unital(self) -> bool:
        id_ = np.arange(len(self.table))
        if (row_comp := (self.table == id_).all(1)).any():
            i = np.argmax(row_comp)
            return (self.table.T[i] == id_).all()
        return False
    def is_abelian(self)  -> bool:
        return (self.table == self.table.T).all()
    
    
class Magma(FinBinOp):
    def __init__(self, table:np.ndarray, strict:bool = True):
        if strict and 
            raise TypeError('pased array must have int values in [0, len - 1]')
        super().__init__(table, strict)        
    def _op_(self, i:int, j:int) -> MagmaElem:
        return MagmaElem(self.table[i,j])

class MagmaElem(int):
    def __init__(self, x:int, magma:Magma):
        self.magma = magma
    def __mul__(self, other:int):
        if isinstance(other, MagmaElem):
            
        
        

        
            
            
        


class Magma:
    def __init__(self, table:pd.DataFrame, elements:list = None):
        assert (x := set(table.index)) == set(table.columns)
        assert x == set(range(l := len(x)))
        self.table = table
        if elements:
            assert len(elements) == l
            self.translate = elements
        assert self.is_closed()
        if any(dups := self.table.duplicated()):
            cdups = self.table.T.duplicated()
            if any(dups & cdups):
                
            self.table = self.table[~cdups & dups
        attrs = []
        attrs.append(self.is_inversive())
        attrs.extend(self.is_assoc_unital())
        if not attrs[-1]:
            self.identity = len(self.table)
            self.table.iloc[len(self.table),:] = 
            
        if all(attrs):
            self = Group(self)
        elif all(attrs[:-1]):
            self = Monoid(self)
        elif atytrs[0]
        
    def is_closed(self) -> bool:
        return set(self.table.values) == set(range(len(table)))

    def is_assoc_unital(self) -> (bool, bool):
        endos = {}
        unital = False
        ident = list(range(len(self.table)))
        for _, row in in self.table.iterrows():
            endos.add(Endo(row))
            if list(row) == ident: unital = True
        for f, g in product(endos, repeat = 2):
            if {g(f), f(g)} <= endos:
                continue
            return False, unital
        return True, unital

    def is_inversive(self) -> bool:
        return np.prod(self.table.values == self.table.T.values)

    def is_unital(self) -> bool:
        
                
        
    
class FinMagma(FinBinop):
    def __init__(self, *args, **nargs):
        super().__init__(*args, **nargs)
        assert set(self.columns) == set(self.index)
        assert self.is_closed()




class GroupDict(dict):

        self.is_closed()





def get_id(o: FinBinOp) -> Any:
    i = {}
    for args, res in o.items():        
        if res in args:
            i.add(args.pop() if (e := args.pop()) == res else e)
            if len(i) > 1: return None
        elif set(args) & i: return None
    return i.pop()

def is_assoc(o: FinBinOp) -> bool:
    pass
    
    
    
def is_group(o:FinBinOp, i):
    if i in 
    if not is_closed(o): return False

    
'''define groups entirely in terms of type classes.

a type G is grouplike if it has

G.sup() -> Type
G.is(x:Type) -> Bool; if G.sup().eq(G, x)
G.eq(a:G, b:G) -> Bool
G.action(a:G, b:G) -> G

-- can have a partial order of these and return the gcd... could even
   define partial/approx groups this way, as a heirarchy of types,
   with certain features falling away at each level

and has these methods for an instance a:G

 a.type() -> Type
   with G.sup().eq(a.type(), G)
 a.inv() -> G:
   with G.eq(a.inv().inv(), a)
 a.id() -> G:
   with G.eq(a.id().inv(), a.id())
        G.eq(G.action(a.id(), a), a)

such that

IF G.sup().eq(b.type(), a.type(), c.type()) & \
   G.eq( id := a.id(), b.id(), c.id())
THEN
   G.eq(G.action(a, b.id()), a)
   G.eq(G.action(b, a.id()), b)
   G.eq(G.action(G.action(a, b), c), G.action(a, G.action(b, c)))

use function class and redef __eq__:
x.__code__.co_code == y.__code__.co_code

if we can ensure that we can *always* write a binary operator as a function,
then associativity should follow from function composition.

so what about rock paper scissors prevents us from writing these binops as functions?

r(x) = r if x==s else x
p(x) = p if x==r else x
s(x) = s if x==p else x

(r * p) * s = p * s = s   =/=   r * (p * s) = r * s = r

s(r(p)) != p(s)(r)



what about addition

a(x) = a.value + x
b(x) = b.value + x
c(x) = c.value + x

(a + b) + c = c(a(b.value))
a + (b + c) = a(b(c.value))

no reason these should be equal, in general

associativity of binops ---> result is invariant of a permutation of function application

are many-many maps associative under composition?



 a.id(x: type(a)) -> type(a); 
    G.eq(a.act(a.id()), a.id().act(a)) and 
    G.eq(a.id(), a.inv().act(a), a.act(a.inv()))


 a.act(b: type(a)) -> type(a)

1. closure ensured by sig of a.act
2. a.id().eq(b.id())


if type(b) == type(a) and 


if a.id().eq( b.id() ) and 



a.id(b.id()).eq( b.id(a.id()) ) an a.id(b.id()).eq



 .action(x(): Endo[X] )
 type a(): X -> X
2. each map knows its identity a.




2. a o (b o c) = (a o b) o c forall a,b,c in type X -> X
3. exists 1(): X-> X, st 1(a()) = a(1()) = a()
4.


 lambda x: (a * b)(x)



 is associated with a map, returns 


dynamic group law:

id() -> Any: identity today
in(x: Any) -> bool: is an element (or its function) in the group
act(x:Any, y:Any) -> Any: returns product

'''
