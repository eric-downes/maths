'''
check this stuff out: https://www.cs.nott.ac.uk/~pszgmh/monparsing.pdf

in future could redef __getattribute__ with a decorator so we can do this:

f.g.h = f *o* g *o* h

... or just use coconut? could check if its performant
'''

from typing import *
import operator as op
import functools as ft
import multiprocess as mp

FScalar = Callable[[Any], Any]
BinOp = Callable[[Any,Any], Any]

class Infix:
    # see: https://code.activestate.com/recipes/384122/
    # https://www.mathcs.emory.edu/~valerie/courses/fall10/155/resources/op_precedence.html
    # https://docs.python.org/3/reference/expressions.html
    def __init__(self, function):
        self.function = function
    def __call__(self, value1, value2):
        return self.function(value1, value2)
    # these allow us to use |..| -- if binops in a lattice (eg boolean) comment out...
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    # these allow *..* -- if your binops are in a ring, comment out
    def __rmul__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))    
    def __mul__(self, other):
        return self.function(other)
    # allow <<..>> -- probably ok for most high level purposes
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)

# example of using the above for composition:
def compose(f, g):
    def comp(x): return f(g(x))        
    return comp
o = Infix(compose)
f = lambda x: x + 1
g = lambda x: x ** 2
h = lambda x: x // 3
assert ((f *o* g) *o* h)(22) == (f *o* (g *o* h))(22)
