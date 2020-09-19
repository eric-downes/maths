# Grant Hubbard's thesis:
# https://pdfs.semanticscholar.org/498c/57b589b4109cea874e3cd994fa646eba2be4.pdf

from pynverse import inversefunc
from functools import partial
from typing import *
import numpy as np
import math

'''
GH Chapter 2... mostly definitions; this code likely buggy completely untested

Here is my interpretation of GH's work so far.  For a python class
implementing this, see the bottom.
'''

# Take two lists of n real numbers with the same len
x = [1, -22, np.pi, 6.6]
y = [10, 200, 33.3, 7e22]
Num = Union[int,float]

'''
Treating these lists as vectors, we can calculate the euclidean
inner product, and associated norm (denoted |x| by GH):
''' 
def euclid_prod(x: Iterable[Num], y: Iterable[Num]):
    assert len(x) == len(y)
    return sum(x[i] * y[i] for i in range(len(x)))
assert np.dot(x, y) == euclid_prod(x, y)

def euclid_norm(x: Iterable[Num]): 
    return math.sqrt(euclid_prod(x, x))

''' 
We can "normalize" a list to be on the surface of a unit
hypersphere centered at zero, if we

1. subtract the column mean -> center it on zero
2. constrain it's euclid norm to be 1
'''
def euclid_normalize(x:Iterable[Num]):
    n = euclid_norm(x)
    return [x_i / n for x_i in x]
assert euclid_norm(euclid_normalize(y)) == 1

''' 
Gloss on the above:
  x^2 + y^2 + z^2 + ... = 1, not true *before* we normalize
So if we have a normalization target, and an equation where a sum == +/- 1
we apply the norm n(x) and then solve the equation



1. Why stop at spheres?

2. Note that the == 1 is implicit after we have normed

we can do all of this with simplexes and the 1-norm, or any power.
In fact we can do this with any function that has an inverse;
for more on pynverse see https://pypi.org/project/pynverse/
the page on copulas provides many examples of archimedean copulas / norms: 
https://en.wikipedia.org/wiki/Copula_(probability_theory)#Archimedean_copulas
'''
def p_norm(x:Iterable[Num], p:Num):
    return sum([x_i ** p for x_i in x]) ** (1 / p)
assert np.array(x) / p_norm(x, 3) == -1

def archimedes_norm(x:Iterable[Num][Num], f:Callable[Num, Num], *args):
    finv = inversefunc(partial(f, *args))
    return finv(sum([f(x_i) for x_i in x]))
assert abs(np.prod(x) - archimedes_norm(x, math.log)) < 1e-6


'''
What about hyperbolas?

First we need the lorentz inner product denoted by GH as $x\circ y$
x1 * y1  +  x2 * y2  +  x3 * y3  +  ...  -  xn * yn

Why the asymmetry?  The last coordinate is time, and we are
using "spacelike coordinates".

I'll avoid thorny issues about "what is time" and "what is space", but 
1. they are *not independent* in relativity, which has hyperbolic structure
2. time coordinate is still "special", even if we ignore arrow-of-time issues

so perhaps if we guess a time coordinate it should be special somehow and not
independent of the other coords.
'''
def _lorentz_hlpr(x:list, ti:int) -> Iterable[Num]:
    return x[:ti] + x[ti+1:]

def lorentz_prod(x:list, y:list, t:Tuple[Num,Num] = None, ti:int = -1):
    if t is None:
        f = partial(_lorentz_hlpr, ti = ti)
        tsq = x[ti] * y[ti]
    else:
        f = lambda x:x
        tsq = t[0] * t[1]
    return euclid_prod(f(x), f(y)) - tsq

''' 
Defining the lorentz norm for lists of complex numbers involves
order-of-operations questions I am happy to dodge.  Grant Hubbard has
only defined these things for lists of reals, and we will take him at
his word, until proven otherwise.

Define the lorentzian norm, which GH calls ||x||:
'''
def lorentz_norm(x:Iterable[Num], t:Num = None, ti:int = -1):
    if t is None:
        t = x[ti]
        f = partial(_lorentz_hlpr, ti = ti)
    else:
        f = lambda x:x
    return lorentz_prod(f(x), f(x), (t, t)) ** (1/2)


''' 
Note that there is a possibility, given a large enough t, for the
lorentz norm to be imaginary even if its arguments are real.  Thus I
have used ** (1/2) instead of math.sqrt; aside: it turns out math.sqrt
is slow compared to ** (1/2)... 100+ ns vs 7 ns



Sect 2.2.5

GH says that this is a hyperbolic equation:

x^2 + y^2 - z^2 = -1

For this projection, we make two changes from the sphere, acording to GH:
 1. we use the lorentz norm, instead of the euclid norm
 2. we divide each x_i /= - lorentz_norm(x)

There are three ways to do that, though... unlike the previous examples,
so I have parametrized it, the index of the time variable
'''
def lorentz_normalize(x:Iterable[Num], t:Num = None, ti:int = -1, mult:int = 1):
    n = mult * lorentz_norm(x, t, ti)
    return [x_i / n for x_i in x]
assert lorentz_norm(lorentz_normalize(x)) == 1

lorentz_normalize(x, mult = -1)






'''
for turning this into a jupyter notebook with latex
https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Working%20With%20Markdown%20Cells.html

# for group theory stuff, some useful stuff we could build on:
python3 -m pip install -e https://github.com/Smeths/pygroup.git

# potentially useful packages i'm not using yet we should look at
import einsteinpy
import pymanopt
import hyperbolic
import vectors

'''

class Vector(np.array):
    # cartesian coordinates assumed throughout
    # do we want to be really strict about "norm cant change"?
    # for now, it can.    
    def euclid_norm(self):
        return math.sqrt(.dot(self))
    def lorentz_norm(self):
        return math.sqrt(self.odot(self))
    def euclid_dist(self, other):
        return math.sqrt(sum(map(lambda x: x**2, self.__array__() - other)))
    
    # lorentzian inner product
    # we assume that the last coord is timelike?
    # should make an explicit constructor for this
    def odot(self, other: Iterable[Num], right:bool = False, conj:bool = True):
        if len(self) != len(other): raise(f'lengths neq')
        l,r = (self,other) if right else (other,self)
        dotf = np.vdot if conj else np.dot
        
        np.vdot(l[:-1], r[:-1]) - (l[-1] * 1j) * (r[-1] * 1j)
        np.dot(self[:-1], map(f, other[:-1])) - self[-1] * f(other[-1])
        xy = [self[i] * y[i] for i in range(len(self))]
        xy[-1] = -1 * xy[-1]
        return sum(xy)
    
    # eq. 2.10 ... if they arent qm-states why are we using kets in def?
    # we need to check with GH on this.
    # also < phi | psi > == < psi | phi > ... 
    # but until we learn otherwise thats what I'm doing!
    # so elliptic dist is == acos( pearson's rho )
    def elliptic_dist(self, other):
        return math.acos( self.dot(other) / (
            self.euclid_norm() * other.euclid_norm() ))

    # again, seems like <a|b> == <b|a> ... 
    def hyperbolic_dist(self, other):
        return math.acosh( self.odot(other) / (
            self.lorentz_norm() * other.lorentz_norm() ))

Real = Union[int, float]

def spinor(alpha:Real, beta:Real, gamma:Real):
    return np.array([[gamma, complex(alpha, -beta)],
                     [complex(alpha, beta), -gamma]])


