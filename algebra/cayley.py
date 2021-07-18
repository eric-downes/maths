from typing import *

state = ((1,2,3,4),5)
generators = {
    'r': lambda s: ((s[0][i] for i in [3,0,1,2]), s[1]),
    'p': lambda s: ((s[1], s[0][1:]), s[0][0]),
    }

def explore(state:tuple, gens:Dict[str,Callable], graph:dict = None) -> Dict[int,[str,tuple]]:
    if graph is None: graph = dict()
    if state not in graph.keys(): graph[state] = dict()
    queue = set()
    for k, v in gens.items():
        if k in graph[state].keys(): continue
        new = v(state)
        graph[state][k] = new
        if new in graph[state].keys(): continue
        queue.add(new)
    for e in queue:
         explore(e, gens, graph)

