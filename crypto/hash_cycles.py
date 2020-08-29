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
from operator import not_
from hashlib import blake2b
import multiprocessing as mp
from functools import partial

if not os.path.isdir('hendo'): os.mkdir('hendo')

def trycept(f, *args, default = None, raize = False, **nargs):
    try: f(*args, **nargs)
    except Exception as e:
        if raize: raise e
        return default

def blake(x:bytes, nbytes:int) -> bytes:
    return blake2b(x, digest_size = nbytes).digest()

def edge(x:int, f:Callable[bytes,bytes]):
    x = x.to_bytes(L,'big')
    return (x, f(x))

def gen_edges(L:int) -> Dict[bytes,bytes]:
    with mp.Pool(mp.cpu_count() * 3 // 4) as p:
        g = partial(edge, f = partial(blake, nbytes = L))
        edges = p.map(g, range(2 ** L))
        edge_dict = {t[0]:t[1] for t in edges}
        pickle.dump(edge_dict, f'hendo/{L}_full.pkl')
        return edge_dict

if __name__ == '__main__' and trycept(not_, __IPYTHON__):
    gen_edges(sys.argv[1] if len(sys.argv) > 1 else 1)
