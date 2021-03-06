#!/usr/bin/env python
"""spanner.py

General purpose pipeline tool.
"""

import os
import sys
import pprint
import argparse

import pltools
import read_from_dir as rfd
from rawimporter import import_files

def dataset_from_dir_name(data_dir, pl):
    dataset_name = os.path.basename(data_dir)
    return pltools.dataset_from_dir(dataset_name, data_dir, pl)

def wrun_pipeline(pl, ds):
    pl.gather_work(ds)

def run_pipeline(pl, ds):
    pl.run(ds)

def run_single_track(ds, name, pl):
    try:
        dt = ds.dtracks[name]
    except KeyError:
        print "ERROR: No such data track %s in dataset %s" % (
            name, ds.name)
        sys.exit(2)

    pl.run_single_track(dt)

def print_data(pl, ds):
    d = ds.get_data()
    pprint.pprint(d)

def plot_pipeline(pl, output_file):
    #try:
    #    import plotpipe
    #except ImportError:
    #    raise

    plotpipe.draw_pretty(pl, output_file)

def main():
    sys.path.insert(0, '/usr/local/lib/python2.7/site-packages/')
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help="command to run")
    parser.add_argument('pipeline', help="pipeline file to load")
    parser.add_argument('-d', '--datadir', type=str, help="directory containing data files")
    parser.add_argument('-o', '--output', type=str, help="output file")
    args = parser.parse_args()

    pl = pltools.load_pipeline_by_name(args.pipeline)

    command = args.command

    if command == 'plot':
        outfile = args.output
        if outfile == None:
            print "ERROR: Must supply an output file with -o"
            sys.exit(2)
        plot_pipeline(pl, outfile)
        sys.exit(0)

    if command == 'list':
        data_dir = args.datadir
        ds = dataset_from_dir_name(data_dir, pl)
        print_data(pl, ds)
        sys.exit(0)

    if command == 'run':
        data_dir = args.datadir
        ds = dataset_from_dir_name(data_dir, pl)
        run_pipeline(pl, ds)
        sys.exit(0)

    if command == 'mrun':
        data_dir = args.datadir
        dss = pltools.multiple_datasets_from_path(data_dir, pl)
        for ds in dss:
            pl.run(ds, noop=False)
        sys.exit(0)

    if command == 'wrun':
        data_dir = args.datadir
        ds = dataset_from_dir_name(data_dir, pl)
        wrun_pipeline(pl, ds)
        sys.exit(0)

    if command == 'import':
        input_dir = args.datadir
        import_files(input_dir, 'data')
        sys.exit(0)


    print "Command not recognised"

    #plname = 'simpip'
    #data_dir = 'data/newexp'



if __name__ == '__main__':
    main()
