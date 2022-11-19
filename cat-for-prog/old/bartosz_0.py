from typing import *
from eric import trycept

# 0.1 Implement, as best as you can, the identity function in your
# favorite language (or the second favorite, if your favorite language
# happens to be Haskell).
def id(x): return x

# Implement the composition function in your favorite language. It
# takes two functions as arguments and returns a function that is
# their composition.
def compose(f: Callable, g: Callable):
    return lambda x: f( g( x ))

# Write a program that tries to test that your composition function
# respects identity.

type_homset = dict()
for t in types:
    type_homset[t] = {y:y for y in types if trycept(y, get_value(t), retval=False)}

def get_value(t : type):
    try: return t()
    except: return t([])
        
def test_compose_id(hset: Dict[type,Dict[type,Callable]] = types_homset):
    for i in hset.keys():
        for j in hset.keys():
            f = hset[i][j]
            jval = get_value(j)
            ival = f( jval )
            assert(compose(f, id)( jval ) == ival)
            assert(compose(id, f)( jval ) == ival)
    return True
test_compose_id()

# Is the world-wide web a category in any sense? Are links morphisms?
'''
yes.  objects: pages, morphisms: links
BUT "remaining on a page" is the identity because not every page has a
link to itself
'''

# Is Facebook a category, with people as objects and friendships as morphisms?
'''
no.  
friendship not transitive a->b * b->c =/=> a->c

can be made a category if you reduce friendships to link-following as
we did above, iff every page with friendhip link in homset is viewable
'''

# When is a directed graph a category?
'''
1. it needs self-links
2. nothing accumulated along the following of an edge not present at the node

could equip networkx / graphviz with knowledge of categories... would that helpm
with forensic graphs? maybe could make a new graph generator "free category"
'''

