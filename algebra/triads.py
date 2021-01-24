'''
implement classes for each group, here:
https://johnkerl.org/doc/kerl-pyaa.pdf

then take a shot at implementing generic group class, given 
(a) cayley diagram
(b) multiplication table
(c) ???


if i have a finite group with a total order, i should be able to
bootstrap (rounded) division by an integer.

within any given orbit i should be able to do similarly

even a path... how would you "divide" an element of the group S_3?

 a -> b -> c -> a...
 |    |    |    
 a' <-b' <-c' <- a'... 

Let horizontal hops be 1s and vertical hops be 0s. If I start at a,

   (a, [11]) == (c, [])

if I provide the sequence [1101] then 

   (a, [1101]) / 2 = (c, [])

It seems like this must work for groupoids/magmas too if they have partial orders..


'''
from typing import *

'misc fcns'

def trycept(f, *args, retval=None, **kwargs):
    try: return f(*args, **kwargs)
    except: return retval

'classes'
    
class Triad:
    def __init__(self,
                 cod:type,
                 m:Union[Callable[[Any,Any], Any], Counter, dict] = None
                 dom:set = set()):
        # is every type a constructor?
        # how can I do type checking genericly?        
        self.cod = t
        self.dom() = (lambda:dom) if callable(m) else (lambda:set(m.keys()))
        self.default = t()
        def y0(y): return self.default if y is None else y
        if not (dom and m): m = t
        else: [assert type(m(x)) == t for x in self.dom()]
        if callable(m):
            self.map = lambda x, y: trycept(m, x, y0(y))
            self.count = None
        else:
            self.count = Counter(m)
            self.map = lambda x, y: self.dict.get(x, y0(y))
    def __call__(self, x, dflt = None):
        return self.map(x, dflt)
    def add(self, other:Triad, default = 0, inplace:bool = False):
        if other.cod != self.cod: raise TypeError(f'codomains must be the same')
        if not (self.count or other.count):
            f = lambda x: self.map(x) + other.map(x)
        elif self.count and other.count:
            (f := (+self.count + +other.count)).subtract(-self.count + -other.count)
        else:
            p = (self.count, other.map) if self.count else (other.count, self.map)
            f = Counter({k: v + p[1](k) for k,v in p[0].items()})
        if inplace:
            self.map = f
            if callable(f):
                (d := self.dom()).update(other.dom())
                self.dom = lambda:d
            else:
                self.dom = lambda:set(self.map.keys())
        else:
            return Triad(self.cod, f, self.dom() | other.dom())

class FinTriad(Triad):
    def __init__(self, cod:type, f:dict = None, dom:set = None):
        if dom is None: super().__init__(cod, lambda x:0, set())
        elif f is None: super().__init__(cod, lambda x:1, dom)
        else: super().__init__(cod, f, dom)
    def raise_from(self, cod:type, dom:set):
        super().__init__(cod, (lambda x:1), dom)
    def push_fwd(self, along:dict, default = 0):
        # implicitly assumes cod is a field...
        # implement more efficient version using dynamic programming
        # see if i can connect it to TDB's work...
        denom = Counter(along.values())
        fwd = defaultdict(lambda: default)
        for k,v in along.items():
            fwd[v] += self.count[k] / denom[k]
        return FinTriad(self.cod, fwd, fwd.keys())
        
