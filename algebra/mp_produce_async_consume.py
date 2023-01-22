import asyncio
import asyncstdlib
import  multiprocessing as mp


def producer_func(todo:Callable,
                  enqueue_condition:Callable[[Any,..],bool],
                  worker_id:int,
                  consumer_queue:mp.Queue,
                  finished_queue:mp.Queue,
                  on_else:Callable[[Any,..],None] = lambda x:None,
                  **kwargs):
    if enqueue_condition(result := todo(**kwargs)):
        consumer_queue.put(result)
    else:
        on_else(result)
    finished_queue.put(worker_id)

async def consumer_base(todo:Callable[[Any],..], None], q:asyncio.Queue):
    while True:
        data = await q.get()
        todo(data)
    
def produce_data(producer_todo:Callable,
                 enqueue_condition:Callable[[Any, ..], bool],
                 kwarg_iterator:Iterator[dict[str, Any]],
                 consumer_todo:Callable,
                 producer_on_else:Callable = lambda x:None,
                 n_consumers:int = 10):
    workers = {}
    conq = mp.Queue()
    finq = asyncio.Queue()
    
    curried = ft.partial(producer_func, todo = producer_todo,
                         enqueue_condition = enqueue_condition,
                         on_else = producer_on_else,
                         consumer_queue = conq, finished_queue = finq)
    for 
    for wid, kwarg_dict in enumerate(kwarg_iterator()):
        kwarg_dict['worker_id'] = wid
        p = mp.Process()
        p.run(target = curried, args = (wid,), kwargs = kwarg_dict)
        p.start()
        workers[wid] = p

    while workers:
        while not conq.empty():
            
        
while producers:
    while not q.empty():
        q.
        
        
