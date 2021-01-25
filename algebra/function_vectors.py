from typing import *
import operator as op
import functools as ft
import multiprocess as mp

import o, Infix from fcn_monoid

class X(object): # use this to define whatever your objects are
    def __call__(): return None
F = Callable[[X], X]
BinOp = Callable[[X, X], X]
Flist = List[F]
UF = Union[F, Flist]

def inclusion(a) -> list:
    # raise object into list algebra
    return a if isinstance(a, list) else [a]
    
def broadcast(a, n:int, left:bool=False) -> list:
    # more general inclusion; "beta" in paper
    x = inclusion(a)
    if left: return x * n
    else: return ft.reduce(op.add, [[e] * n for e in x])

def zipxtd(x, y, retzip:bool=False) -> Union[list, zip]:
    # pair l and r; broadcasting as necessary
    # basically a flattened cartesian product of lists
    l = inclusion(x)
    r = inclusion(y)
    if len(l) = len(r): z = zip(l, r)
    else: z = zip(l * len(r), broadcast(r, len(l)))
    return z if retzip else list(z)

def apply(f, *args, retval:bool = X(), raize:bool=True):
    try: return f(*args)
    except Exception as e:
        if raize: raise e
        return retval

def applyxtd(fs:UF, xs, mproc:bool=False) -> List[X]:
    # apply a function to a list of arguments, using broadcasting
    fx = zipxtd(inclusion(fs), inclusion(xs))
    if mproc:
        with mp.Pool() as p:
            out = p.map(apply, fx)
    else:
        out = list(map(apply, fx))
    return out

def sumxtd(fs:UF, xs:list) -> X:
    return sum(applyxtd(fs, xs))

def prodxtd(fs:UF, xs:list) -> X:
    return ft.reduce(op.mul, applyxtd(fs, xs))

def kappa(bop:BinOp, fs:UF) -> Callable[[List[X]], X]:
    return lambda x: ft.reduce(bop, applyxtd(fs, x))

