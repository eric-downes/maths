'''
implements the simplest heyting algebra:

F < ? < T

a -a
F T
? F
T F

a & b
  F ? T
F F F F
? F ? ?
T F ? T

a | b
  F ? T
F F ? T
? ? ? T
T T T T

use a <= b for b -> a

would like a general constructor for distributive lattices & symmetric
monoidal preorders... see 7 Skeches Ch 1

would really like a class that allows this:
```
from heyting import Maybe, implies


```

'''

def implies(l, r):
    if l is True: return True
    if l is False: return r
    return l <= r

def test():
    assert(not Maybe == False)
    assert(Maybe == True and Maybe)
    assert(Maybe == Maybe or False)
    assert(Maybe == implies(True, Maybe))
    h = [False, Maybe, True]
    for x in h:
        assert(True == implies(x, x))
        for y in h:
            i = implies(x, y)
            assert(x and i == x and y)
            assert(y and i == y)
            for z in h: 
                assert(implies(x, y and z) == i and implies(x, z)) 

class Heyt:
    def __init__(self, val: Union[Bool, Heyt] = False):
        self.value == val
        return self



    def __eq__(self, x): return x == self.value
    def __or__(self, x: Union[Bool, Heyt]):
        if x == True: return Heyt(True)
        if x == False: return Heyt(x)
        return 
            
    def __abs__(self): return {False:0, Maybe:.5 True:1}[self.value]
    def __add__(self, x): return self.__abs__() + x
    def __bool__(self, maybe_default=True):

 '__xor__',
 '__and__',
 '__or__',
 '__radd__',
 '__rand__',

 
['__abs__',
 '__

 '__bool__',
 '__ceil__',
 '__class__',
 '__delattr__',
 '__dir__',
 '__divmod__',
 '__doc__',
 '__eq__',
 '__float__',
 '__floor__',
 '__floordiv__',
 '__format__',
 '__ge__',
 '__getattribute__',
 '__getnewargs__',
 '__gt__',
 '__hash__',
 '__index__',
 '__init__',
 '__init_subclass__',
 '__int__',
 '__invert__',
 '__le__',
 '__lshift__',
 '__lt__',
 '__mod__',
 '__mul__',
 '__ne__',
 '__neg__',
 '__new__',

 '__pos__',
 '__pow__',

 '__rdivmod__',
 '__reduce__',
 '__reduce_ex__',
 '__repr__',
 '__rfloordiv__',
 '__rlshift__',
 '__rmod__',
 '__rmul__',
 '__ror__',
 '__round__',
 '__rpow__',
 '__rrshift__',
 '__rshift__',
 '__rsub__',
 '__rtruediv__',
 '__rxor__',
 '__setattr__',
 '__sizeof__',
 '__str__',
 '__sub__',
 '__subclasshook__',
 '__truediv__',
 '__trunc__',

 'as_integer_ratio',
 'bit_length',
 'conjugate',
 'denominator',
 'from_bytes',
 'imag',
 'numerator',
 'real',
 'to_bytes']


                

def LE(l, r):

class Heyt:
    def __init__(val:None):
        if val is True: self.value = '1'
        if val is None or val is False: self.value = '0'
        
            


def heyting_and(l:Union[Heyt, Any], r:Union[Heyt, Any]) -> Heyt:
    
