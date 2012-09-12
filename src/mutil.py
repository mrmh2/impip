import os
import errno

def mkdir_p(path):
    try:
        os.makedirs(path)   
    except OSError as exc:
        # FIXME
        if exc.errno == errno.EEXIST:
            pass
        else: raise


