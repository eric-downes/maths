import typing
import inspect
import numpy as np

def sample_values(thetype:type, size:int=4, maxv:int=22):
    if thetype is int:
        return np.r_[0, 1, -1, np.random.randint(2, maxv, size=size)]
    elif thetype is str:
        return np.r_[0, 1, np.random.choice(
    elif thetype is float:
        return np.r_[


class MorphismGenerator:
    def __init__(self, generator:type(lambda:1), domain:type, codomain:type):
        self.code = inspect.getsource(generator)

class Category:

    def __init__(self, objects=set(), morphs=dict(), identity=None):
        if identity is None: identity = self._id
        self.id = identity # need to curry identity to include strict if they dont pass it...
        self.objs = objects
        self.maps = morphs # non-id morphisms only

    def _id(self, x, strict=True):
        if strict and x not in self.objs: return np.nan
        return x

    def add_object(self, x):
        self.objs[ str(x) ] 






    
    def test(self, obj_subset=None, map_dict=None, strict=False):
        if obj_subset is None: obj_subset = self.objs
        if map_dict is None: map_dict = self.maps
        dont = set()
        while obj_subset:
            source = object_subset.pop()
            if source != self.id(source):
                print(f'object {o} failed Identity test!')
                return False
            dont.add(source)
            for target in object_subset:
                for f in map_dict[ source ][ target ]:                    
                    for g in self.maps[ target ].values():
                        g( f(source) )
                    a = g( f(source) )


                map_dict[source].keys():
                


            set(self.maps[o].keys()).intersection(target_subset):
                

            passed:
                self.maps[o]

            
all objects in subset pass identity test')

        if any({o 
        

        
class BloomFilter:

    def __init__(self, n=50, ptarget=1e-6, nTweak=22):
        self.filter = CBloomFilter(n, ptarget, nTweak, CBloomFilter.UPDATE_ALL)

    'I/O'
        
    @classmethod
    def from_attributes(cls, vData, n_hash_funcs, n_tweak, n_flags=0):
