# 用装饰器实现 log

from functools import wraps
import time
from MyToolKit.logger import MyLogger 

def logg(func):
    logger = MyLogger("./debug.log")
    logger.info("Execute:", func.__name__)
    @wraps(func)
    def log_func(*args, **kwargs):
        tic = time.time()
        kwargs["logger"] = logger
        g = func.__globals__
        g["print"] = logger
        res = func(*args, **kwargs)
        toc = time.time()
        logger.info("Done , cost time:{0:2f}".format(toc-tic))
        return res
    return log_func


if __name__ == "__main__":
    @logg
    def test(a, b, logger=None):
        print(a)
        print(b)
        return a+b
    test(1,2)



