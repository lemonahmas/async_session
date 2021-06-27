import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        name = func.__name__
        BT = time.time()
        print(f"Timing this func: {name} -- Aa")
        func(*args, **kw)
        ET = time.time()
        ret_str = f"This func:{name} took: "+str(ET-BT)+" seconds"
        print(ret_str)
    return wrapper