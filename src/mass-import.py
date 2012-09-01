#!/usr/bin/env python

import os, sys, shutil
import re

def sorted_nicely( l ):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)

def conv_name(import_path, f, i1, i2):

    cn = f[i1:i2]

    return os.path.join(importpath, cn + '.png')

def myfil(f):
    if f.find('plantD') != -1: return True
    else: return False

def pngfil(f):
    b, e = os.path.splitext(f)
    if e == '.png': return True
    else: return False

def do_stuff_n(importdir, importpath):

    ifiles = sorted_nicely(filter(pngfil, os.listdir(import_dir)))
    files = filter(myfil, ifiles)

    fnames = ["T%02d.png" % i for i in range(0, len(files))]

    ffiles = [os.path.join(import_dir, f) for f in files]
    tofiles = [os.path.join(importpath, f) for f in fnames]

    fn = zip(ffiles, tofiles)
    
    for f, t in fn:
        print 'cp', f, t
        shutil.copy(f, t)

try:
    import_dir = sys.argv[1]
except IndexError, e:
    print "Usage: %s import_dir" % os.path.basename(sys.argv[0])
    sys.exit(1)

importpath = 'data/newexp/segmented_image'
do_stuff_n(import_dir, importpath)

#importpath = 'data/oldexp/rotated_image'
#do_stuff_n(import_dir, importpath)

#importpath = 'data/oldexp/rotated_projection'
#do_stuff_n(import_dir, importpath)
