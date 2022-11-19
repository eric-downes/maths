import functools
from typing import *
import eric 

'''
Define a higher-order function (or a function object) memoize in your
favorite language. This function takes a pure function f as an
argument and returns a function that behaves almost exactly like f,
except that it only calls the original function once for every
argument, stores the result internally, and subsequently returns this
stored result every time it’s called with the same argument. You can
tell the memoized function from the original by watching its
performance. For instance, try to memoize a function that takes a long
time to evaluate. You’ll have to wait for the result the first time
you call it, but on subsequent calls, with the same argument, you
should get the result immediately.
'''

# attaching a dict to the function object works for external calls
def memoize(idict = None):
    def g(x): return g.memo_dict.get(x, f(x))
    g.memo_dict = idict if idict else dict() # this is the cache
    return g

# for recursive functions like fib need to use lru cache fcn decorator
# https://docs.python.org/3/library/functools.html

@functools.lru_cache(maxsize = None)
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)

''' 
Try to memoize a function from your standard library that you
normally use to produce random numbers. Does it work?  
'''
import random
@functools.lru_cache(maxsize = None)
def not_rand(x): return random.random()

'''
Most random number generators can be initialized with a
seed. Implement a function that takes a seed, calls the random number
generator with that seed, and returns the result. Memoize that
function. Does it work?
'''
def rand(x = None):
    if x is not None: random.seed(x)
    return random.random()

''' 
How many different functions are there from Bool to Bool? Can you
implement them all?  
'''

# in the "set function" sense there are 4: 01->(00,01,10,11)
f = lambda x: False
i = lambda x: x
n = lambda x: not x
t = lambda x: True


'''
Draw a picture of a category whose only objects are the types
Void, () (unit), and Bool; with arrows corresponding to all possible
functions between these types. Label the arrows with the names of the
functions.
'''

# absurd functions: Void -> True, Void -> False, Void -> (), Void -> Void
# units: () -> True, () -> False, () -> ()
# bools: T -> (), F -> (), T -> T, T -> F, F -> T, F -> F

from graphviz import Digraph
cat = Digraph(comment='Category with Void, (), Bool')
cat.node('v', 'Void')
cat.node('u', '()')
cat.node('b', 'Bool')
cat.edges(['vv','vu','vb','vb'])
cat.edges(['uu','ub','ub'])
cat.edges(['bu','bb','bb','bb','bb'])
cat #.render('cat.gv',view=True)
