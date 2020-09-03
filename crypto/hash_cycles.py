'''
lets study the endomorphisms of cryptographic hash functions!

TODO:
 * is hashlib.sha3_256 the same as keccak 256 in Monero?, eth?
 * use graphviz to make pretty graphs from the edge dict
 * make an interruptible version that pickles state upon SIGHUP, SIGTERM, etc
'''

import os
import sys
import pickle
from typing import *
from operator import not_
from hashlib import blake2b
import multiprocessing as mp
from functools import partial

ENDIAN = 'big'

def trycept(f, *args, default = None, raize = False, **nargs):
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

def gen_edges(nbytes: int,
              H: Callable[[int,int], Tuple[int,int]]) -> List[Tuple[int,int]]:
    with mp.Pool(mp.cpu_count() * 3 // 4) as p:
        return p.map(blake, range(2 ** (nbytes * 8)))

if __name__ == '__main__' and trycept(not_, __IPYTHON__):
    if not os.path.isdir('hendo'): os.mkdir('hendo')
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    edges = gen_edges(L)
    pickle.dump(edges, f'hendo/{L}B_full.pkl')
