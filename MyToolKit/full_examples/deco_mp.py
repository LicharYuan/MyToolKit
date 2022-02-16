#encoding: utf-8
"""
使用装饰器 把单进程包装成多进程. [x]
装饰器会改变目标函数的地址? 导致pickle出错
所以我们更换成cls来做这件事
"""
from functools import wraps, partial
from multiprocessing import Pool
import copy
import pickle as pkl
from datetime import datetime
import numpy as np
import sys

class MP(object):
    def __init__(self, func, mp_keys, pool_size=2, save=True):
        self.func = func
        assert isinstance(mp_keys, list), "mp_keys should be a list"
        self.mp_keys = mp_keys
        self.pool_size = pool_size
        self.save = True
        self.time = datetime.now().strftime("%y%m%d-%H%M%S")
        self.name = func.__name__

    def __call__(self, *args, **kwargs):
        keys_chunk = [[] for _ in range(len(self.mp_keys))] 
        args_chunk = [args] * self.pool_size
        run_pool = Pool(self.pool_size)
        for j,key in enumerate(self.mp_keys):
                assert key in kwargs, f"{key} not in kwargs"
                values = np.array(kwargs[key])
                values_chunk = np.array_split(values, self.pool_size)
                for i in range(self.pool_size):
                    keys_chunk[j].append(values_chunk[i])

        run_func = partial(self.func, *args)
        res = run_pool.starmap(run_func, zip(*keys_chunk))
        if self.save:
            with open(f"./{self.time}_mp_results.pkl", "wb")  as f:
                pkl.dump(res, f)
            print("saving results in", f"./{self.time}_mp_results.pkl")

        return res

if __name__ == "__main__":

    def single(a, b, c=None, d=None):  
        print(c, d)      
        res = {}
        res["c"] = []
        res["d"] = []

        for ele in c:
            res["c"].append(a*b*ele)
        for ele in d:
            res["d"].append(a*b*ele)
        return res
    
    a = 1
    b = 2
    cc = [[1,2],[3,4]]
    dd = [[5,6],[7,8]]
    print("Loop:")
    for c, d in zip(cc, dd):
        res = single(a, b, c, d)
        print(c, d, "运行结果:", res)
    
    print("add CLS:")
    
    mp_single = MP(single, ["c","d"], 2, True)
    print(mp_single(a, b, c=cc, d=dd)) # 一定要加变量名运行
            
            

            
            

                    
                    







            


            

            




