'''
(Inefficient) Reference Implementation of Cover Thickness and Probability using LatticeCounters

monad maps x to (x,0,1).  Full space is (x,-m,+n) where n,m are on N^2; this is not quite a group
+(x,0,0) is identity morphism for each x, no additive inverse: (x,-m,+n) - (x,-m,+n) = (x, -m-n, m+n)
we can express (x,-m,+n) as x_{n-m} where "-" is used as a dash 2-2 3-3 are all different
the "null line" (n,n) maps to zero when we map to probabilities; 
this is non-monotonic from the usual preorder on N^2
'''

from typing import *
# from sigma_algebra import ProbabilityEngine
from collections import Counter, Defaultdict

class LatticeCounter:

    def __init__(self):
        self.members = Defaultdict(lambda : [0,0])

    def __eq__(self, other:"LatticeCounter") -> bool:
        self.members == other.members
        
    def oplus(self, to_add:"LatticeCounter", pos:bool = True):
        for x in to_add.members.keys():
            self.members[x][True] += to_add[x][pos]
            self.members[x][False] += to_add[x][~pos]
                
    def ominus(self, to_sub:"LatticeCounter"):
        self.oplus(to_sub, pos=False)

    def to_tuples(self) -> List[Tuple[Any,int,int]]: # lossless
        return [(k, *v) for k,v in self.members.items()]

    def to_set(self, pos:bool = True) -> set: # coerce ominus to behave like setdiff; lossy
        return {k for k,v in self.members.items() if v[pos] > v[~pos]}

    def to_bag(self, allpos:bool = False) -> Counter: # collapse (X, +n, -n) --> {}; lossy
        sign = 1 * allpos - 1 * (1 - allpos)
        c = Counter()
        for x in self.members.keys():
            c.update({x: self.members[x][True] + sign * self.members[x][False]})
        return c

    @classmethod
    def from_tuples(cls, ts : Sequence[Tuple[Any, int, int]]) -> "LatticeCounter":
        inst = cls()
        [inst.members[ t[0] ][x] += t[x+1] for t in ts for x in [0,1]]
        return inst
            
    @classmethod
    def from_set(cls, s:set, pos:bool = True) -> "LatticeCounter":
        inst  = cls()
        [inst.members[x][pos] += 1 for x in s]
        return inst
        
    @classmethod
    def from_dict(cls, d:Dict[Any,int]) -> "LatticeCounter":
        inst = cls()
        [inst.members[k][v > 0] = v for k,v in d.items()]
        return inst
        
    @classmethod
    def _test_(cls):
        # from_set monad 
        xset = {'a', 'b', 'c'}
        x = cls.from_set(xset)
        xmem = {'a':(0,1), 'b':(0,1), 'c':(0,1)}
        assert(dict(x.members) == xmem)
        # roundtrip with to_set
        assert(x.to_set() == xset)
        # from_tuples monad 
        y = cls.from_tuples([('a',-1,1), ('b',-1,1), ('c',0,1)])        
        ydict = {'a':(-1,1), 'b':(-1,1), 'c':(0,1)}
        assert(ydict == dict(y.members))
        # oplus test
        yy = y
        assert(dict(yy.oplus({'a','b'}).members) == {'a':(-1,2), 'b':(-1,2), 'c':(0,1)})
        # ominus test
        xx = x
        assert(xx.ominus({'a','b'}) == y)
        if getattr(cls,'prob',False):
            # basic probability test
            p = .2
            prob = ProbabilityEngine()
            prob.define('p(c)', p)
            assert(p == y.prob(prob))
            # manual error estimate test
            prob.define('p(a)', (1 - p)/3 )
            prob.define('p(b)', 1 - (prob.get('p(a)') + prob.get('p(c)')) )
            err = 1e-3
            t = y.prob_err_tuple(err, prob)
            assert(t[0] == p)
            assert(t[1] == 5 * err)

'''
havent finished ProbabilityEngine yet...,

    def prob(self, p_map:ProbabilityEngine, allpos:bool=False) -> float:
        return sum([v * p_map.get(f"p('{k}')") for k,v in self.to_bag(allpos).items()])

    def cover_thickness(self) -> Dict[Any,int]:
        return {k:sum(v) for k,v in self.members.items()}
        
    def prob_err_tuple(self, err:float, p_map:ProbabilityEngine) -> Tuple[float,float]:
        # should implement more sophisticated error handling...
        return (self.prob(p_map), err * self.cover_thickness())

'''
