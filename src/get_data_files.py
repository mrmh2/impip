#!/usr/bin/env python

import os
import sys
import pprint

import simpip
import pipeline
import read_from_dir as rfd

def get_data_files(dataset_name):
    dir_name = 'data'
    data_dir = os.path.join(dir_name, dataset_name)
    ds = rfd.dataset_from_dir(dataset_name, data_dir)
    d = ds.get_data()
    
    return d

def main():
    try:
        dataset_name = sys.argv[1]
    except IndexError:
        print "Usage %s dataset_name" % os.path.basename(sys.argv[0])
        sys.exit(0)
    
    d = get_data_files(dataset_name)

    pprint.pprint(d)

if __name__ == '__main__':
    main()
