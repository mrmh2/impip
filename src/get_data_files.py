#!/usr/bin/env python

import os
import re
import sys
import pprint

import simpip
import pipeline
import read_from_dir as rfd

def sorted_nicely( l ):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)

def get_data_files(dataset_name, time_point=None, pipeline_name='simpip'):
    dir_name = 'data'
    data_dir = os.path.join(dir_name, dataset_name)
    ds = rfd.dataset_from_dir(dataset_name, data_dir, pipeline_name)
    d = ds.get_data()
    
    if time_point is None:
        return d
    else:
        dk = sorted_nicely(d.keys())
        return d[dk[time_point]]

def main():
    try:
        dataset_name = sys.argv[1]
    except IndexError:
        print "Usage %s dataset_name [pipeline_name]" % os.path.basename(sys.argv[0])
        sys.exit(0)

    if len(sys.argv) > 2:
        pl_name = sys.argv[2]
    else:
        pl_name = 'simpip'
    
    d = get_data_files(dataset_name, pipeline_name=pl_name)

    pprint.pprint(d)

if __name__ == '__main__':
    main()
