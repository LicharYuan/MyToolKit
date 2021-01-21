"""script to wrappers"""
from functools import wraps
import time

def get_run_time(func):
    @wraps(func)
    def _run_time(*args, **kwargs):
        tic = time.time()
        print("Call Function:", func.__name__)
        res = func(*args, **kwargs)
        toc = time.time()
        print("Cost time", toc-tic)
        return res
    return _run_time



if __name__ == "__main__":
    @get_run_time
    def add(a,b):
        return a+b

    add(2,1)