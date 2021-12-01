'''
a functor (decorator) to take an annotated callable and its arguments and return values, and map to
Callable[[dict], dict]
while also passing an arg via the decorator argument(s)

'''

from typing import *
import functools as ft

def outer_wrap(name:str) -> Callable:
    def inner_wrap(fcn:Callable) -> Callable[[dict],dict]:
        @ft.wraps(fcn) # alt: `def g(self, d:dict, fcn:Callable) -> dict:`
        def g(self, d:dict) -> dict:
            res = fcn(self, **{k:v for k,v in d.items() if k in fcn.__annotations__})
            return {name: res, 'x': self.x}
        return g # alt: `return ft.partialmethod(g, fcn = fcn)`
    return inner_wrap # alt: `return ft.partial(inner_wrap, name = name)`

n = 'name'
y = 22
class C:
    x = y
    @outer_wrap(n)
    def f(self, a:int, b:int) -> int: return a + b

c = C()
assert (r := {n: 3, 'x': y}) == c.f(d := {'a':1, 'b':2}), "boo hiss; in: {d}; out: {r}"
print('Passed!')
