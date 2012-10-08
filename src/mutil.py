import os
import errno

def mapply(func, it):
    for i in it:
        func(i)

def mkdir_p(path):
    try:
        os.makedirs(path)   
    except OSError as exc:
        # FIXME
        if exc.errno == errno.EEXIST:
            pass
        else: raise


