#!/usr/bin/env python

import os
import sys
import shutil
import itertools

from mutil import mkdir_p

rawexts = ['.lif', '.lsm']

def parse_filename(fn):
    basename = os.path.basename(fn)

    name, ext = os.path.splitext(basename)

    split = name.split('_')

    expid = split[0]
    tp = int(split[1][2:])
    subname = split[2]

    try:
        part = int(split[3])
    except IndexError:
        part = None

    return expid, subname, tp, ext, part

def generate_path(components, pathroot):

    e, s, t, ext, p = components

    path = os.path.join(pathroot, e, s, 'microscope_file')
    if p is not None:
        filename = 'T%02d-%02d%s' % (t, p, ext)
    else:
        filename = 'T%02d%s' % (t, ext)

    return path, filename

def import_files(input_path, output_path):
    pathdata = [(r, fs) for r, d, fs in os.walk(input_path)]
    filelist = [[os.path.join(r, f) for f in fs] for r, fs in pathdata if len(fs)]
    files = list(itertools.chain(*filelist))
    rawfiles = [f for f in files if os.path.splitext(f)[1] in rawexts]

    name_components = [parse_filename(f) for f in rawfiles]
    pathfiles = [generate_path(c, output_path) for c in name_components]
    unique_dirs = set(zip(*pathfiles)[0])

    [mkdir_p(d) for d in unique_dirs]

    copylocs = [os.path.join(d, f) for d, f in pathfiles]

    for f, t in zip(rawfiles, copylocs):
        if not os.path.exists(t):
            print "Importing %s as %s" % (f, t)
            shutil.copy(f, t)

def main():
    try:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
    except IndexError, e:
        print "ERROR: Please supply directory name and output directory"
        sys.exit(2)

    import_files(input_path, output_path)
    
if __name__ == '__main__':
    main()

