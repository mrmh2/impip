#!/usr/bin/env python

import os
import sys

import read_from_dir as rfd
#import simpip

def main():
    try:
        dataset_name = sys.argv[1]
    except IndexError:
        print "Usage %s dataset_name" % os.path.basename(sys.argv[0])
        sys.exit(0)

    if len(sys.argv) > 2:
        p_name = sys.argv[2]
    else:
        p_name = 'simpip'

    pmod = __import__(p_name)
    pl = pmod.create_pipeline()
    dir_name = 'data'
    data_dir = os.path.join(dir_name, dataset_name)
    ds = rfd.dataset_from_dir(dataset_name, data_dir, p_name)

    pl.run(ds)

if __name__ == '__main__':
    main()
