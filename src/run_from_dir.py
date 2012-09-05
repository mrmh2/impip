#!/usr/bin/env python

import os
import sys

import read_from_dir as rfd
import simpip

def main():
    try:
        dataset_name = sys.argv[1]
    except IndexError:
        print "Usage %s dataset_name" % os.path.basename(sys.argv[0])
        sys.exit(0)

    pl = simpip.create_pipeline()
    dir_name = 'data'
    data_dir = os.path.join(dir_name, dataset_name)
    ds = rfd.dataset_from_dir(dataset_name, data_dir)

    pl.run(ds)

if __name__ == '__main__':
    main()
