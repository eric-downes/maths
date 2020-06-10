from typing import *
import pandas as pd
import numpy as np

from bartosz_0 import id

# once you've found a non-trivial default value for each type

types = [\
    pd.DataFrame,
    pd.Series,
    np.array,
    # sympy object ...
    # pymanopt?
    # networkX
    Exception,
    bool,
    bytearray,
    bytes,
    classmethod,
    complex,
    dict,
    enumerate,
    filter,
    float,
    frozenset,
    int,
    list,
    map,
    memoryview,
    object,
    property,
    range,
    reversed,
    set,
    slice,
    staticmethod,
    str,
    super,
    tuple,
    type,
    zip]

def trycept(f, x, retval=None, raize=False):
    try: return f(x)
    except Exception as e: 
        if raize: raise e
        else: return retval

def get_value(t : type):
    try: return t()
    except: return t([])

def make_homset(fcns: List[Callable] ) -> dict:
    homset = defaultdict(lambda : defaultdict(lambda : set())) 
    for f in fcns:
        fd = f.__annotations__.copy()
        out_type = fd.pop('return')
        if len(fd) >= 1: raise ValueError(f'multi-arg fcns not supported yet')
        in_type = fd.values()[0]
        homset[ in_type ][ out_type ] = homset[ in_type ].get(out_type, set()) | {f}
    return homset

def test_03(hset = types_homset):
    for i in hset.keys():
        for j in hset.keys():
            f = hset[i][j]
            jval = get_value(j)
            ival = f( jval )
            assert(compose(f, id)( jval ) == ival)
            assert(compose(id, f)( jval ) == ival)
    return True

