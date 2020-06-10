def trycept(f, args, retval=None, raize=False, kwargs):
    try: return f(*args, **kwargs)
    except Exception as e:
        if raize: raise e
        else: return retval

'''
inlining in python:
https://tomforb.es/automatically-inline-python-function-calls/

wonder if I can fix these issues?

BM on inlining in haskell about halfway through:
https://www.youtube.com/watch?v=EO86S2EZssc

'''
