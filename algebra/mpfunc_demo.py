from typing import *
import functools as ft
from multiprocess import Pool

def test(f:Callable, inp:list, outp:list, name:str) -> list:
    try:
        with Pool() as p:
            out = p.map(f, inp)
    except: out = None
    status = 'OK' if out == outp else 'FAILED'
    print(f'{name}: {status}')

def sq(x:int) -> int: return x**2
test(sq, [1,2,3], [1,4,9], 'basic')
test(lambda x: x**2, [1,2,3], [1,4,9], 'lambda')
test(lambda f: f(2), [ft.partial(lambda x,j: x**j, j=i) for i in range(4)], [1,2,4,8], 'functional')

class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)
    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __rshift__(self, other):
        return self.function(other)
    def __call__(self, value1, value2):
        return self.function(value1, value2)

