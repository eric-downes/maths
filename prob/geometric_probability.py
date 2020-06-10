# https://docs.scipy.org/doc/scipy/reference/optimize.nonlin.html

import numpy as np
from typing import *
from scipy.optimize import newton_krylov, broyden1

def normalize(f:np.array) -> np.array:
    f[ np.isnan(f) ] = 0
    if any(f < 0): f += max(abs(f[f < 0]))
    f /= np.sum(f)
    return f

def _KLD_(q:np.array, r:np.array, p:np.array) -> np.array:
    return np.dot(r, np.log(p) - np.log(q))

def gen_KLD_solver_fcn(k:float, p:np.array, over_p:bool=True) -> Callable:
    if any(p < 0) or np.sum(p) != 1: p = normalize(p)
    if over_p:
        kldw = functools.partial(_KLD_, r=p, p=p) - abs(k) 
    else:
        def kldw(x): return abs(k) - _KLD_(q=x, r=x, p=p)
    return kldw

def bayes_dual(xxin:float, yxin:float): -> Tuple[float,float]:
    # this assumes the outward construction
    # doubles on the curve C = xy; C = joint probability 
    yyout = yxin * xxin

    
        pa:float, pbga:float) -> Tuple[float,float]:
    pb = pa * pbga
    
