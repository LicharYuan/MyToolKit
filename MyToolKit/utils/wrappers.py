"""script to wrappers"""
from functools import wraps
import time

def get_run_time(func):
    print(func.__name__)
    @wraps(func)
    def _run_time(*args, **kwargs):
        tic = time.time()
        print("Call Function:", func.__name__)
        res = func(*args, **kwargs)
        toc = time.time()
        print("Cost time", toc-tic)
        return res
    return _run_time

def get_run_time_v2(stype=1):
    def get_run_time(func):
        @wraps(func)
        def _run_time(*args, **kwargs):
            tic = time.time()
            print("Call Function:", func.__name__)
            res = func(a = stype, *args, **kwargs)
            toc = time.time()
            print("Cost time", toc-tic)
            return res
        return _run_time
    return get_run_time



if __name__ == "__main__":
    @get_run_time_v2(1)
    def add(a,b):
        return a+b

    @get_run_time
    def add_2(a, b):
        return a+b


    

    print(add(b=6))
    print(add_2(1,2))