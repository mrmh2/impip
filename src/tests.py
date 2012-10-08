#!/usr/bin/env python

import os
import itertools

import pltools

from mutil import mapply

def generate_name(basepath, path):
    basename = os.path.basename(basepath)
    return path[path.find(basename):]

def multiple_datasets_from_path(path, pl):

    walk = [(r, ds) for r, ds, fs in os.walk(path) if len(ds)]
    full_dirs_paths = [[os.path.join(r, d) for d in ds] for r, ds in walk]
    dirlist = list(itertools.chain(*full_dirs_paths))

    datasets = [pltools.dataset_from_dir(generate_name(path, f), f, pl) 
        for f in dirlist]

    return [ds for ds in datasets if ds.size]


plname = 'shortpip'
pl = pltools.load_pipeline_by_name(plname)
dss = multiple_datasets_from_path('data/ExpID3078', pl)

def gen_noop_runner():
    def nr(ds):
        return pl.run(ds, noop=True)

    return nr

nr = gen_noop_runner()

mapply(nr, dss)
