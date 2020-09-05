'''
lets study the endomorphisms of cryptographic hash functions!

TODO:
 * record exact diff bet. hashlib.sha3_256 & keccak-256 in Monero?, eth?
 * make an interruptible version that pickles state upon SIGHUP, SIGTERM, etc
 * add an analytics function that counts the number of partitions
 * .. for cycles (connected components?)
 * what graph viz software can handle 16e6 edges? ... 4e9???
 * if we start proc & have ea compte chains, and use shared mem.... could compute
   stats as we go.
 * record avalanche criteria -- change 1 bit, do 50% of output bits change?
 * come up with a "truly" random hendo using random.org...
'''

import os
import sys
import math
import pickle
import pandas as pd
from typing import *
from operator import not_
from hashlib import blake2b
from graphviz import digraph
import multiprocessing as mp
from functools import partial
from scipy.stats import binom

ENDIAN = 'big'
HashFunc = Callable[[int, int], Tuple[int, int]]

def trycept(f:Callable, *args, default = None, raize:bool = False, **nargs):
    try: f(*args, **nargs)
    except Exception as e:
        if raize: raise e
        return default

def blake(x:int, nbytes:int) -> Tuple[int,int]:
    h = blake2b(i2b(x, nbytes), digest_size = nbytes).digest()
    return (b2i(x), b2i(h))

def i2b(x:int, nbytes:int = None) -> bytes:
    if nbytes is None: nbytes = math.ceil(math.log2(x) / 8)
    return x.to_bytes(nbytes, ENDIAN)

def b2i(x:bytes) -> bytes:
    return int.from_bytes(x, ENDIAN)

def gen_edges(nbytes:int, hash_fun:HashFunc) -> List[Tuple[int,int]]:
    h = partial(hash_fun, nbytes = nbytes)
    with mp.Pool(mp.cpu_count() * 3 // 4) as p:
        return p.map(h, range(2 ** (nbytes * 8)))

if __name__ == '__main__' and trycept(not_, __IPYTHON__):
    # setup
    for d in ['hendo','hendo_graphs','hendo_stats']:
        if not os.path.isdir(d): os.mkdir(d)
    view = '--view' in ''.join(sys.argv)
    nB = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    # generate & save data
    edges = gen_edges(nB, blake)
    pickle.dump(edges, f'hendo/blake2b_{nB}B_full.pkl')
    dg = digraph()
    dg.edges(edges)
    dg.render(f'hendo_graph/blake2b_{nB}B_full.gv', view = view)
    # stats
    maps = pd.DataFrame(edges, columns = ['x','hx']).set_index('x')['hx'] 
    primg_hist = maps.value_counts().value_counts()
    primg_hist.loc[0] = len(maps) - primg_hist.sum()
    primg_hist.to_csv(f'hendo_stats/blake2b_{nB}B_full.csv')
