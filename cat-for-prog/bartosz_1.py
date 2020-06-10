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
should get the result immediately.'''

# this works for external calls... but not for recursive fcns...
def memoize(f, idict=None): 
    def g(x): return g.memo_dict.get(x, f(x))
    g.memo_dict = idict if idict else dict()
    return g 

'''
in practice can use @functools.lru_cache e.g. to memoize a recusrive function:
https://docs.python.org/3/library/functools.html
'''

@lru_cache(maxsize=None)
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)

