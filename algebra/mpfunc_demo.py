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

