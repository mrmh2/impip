#!/usr/bin/env python

import os, sys, shutil

def conv_name(import_path, f, i1, i2):

    cn = f[i1:i2]

    return os.path.join(importpath, cn + '.png')

def myfil(f):
    if f.find('plantD') != -1: return True
    else: return False

def do_stuff(importdir, importpath, i1, i2):

    files = filter(myfil, os.listdir(import_dir))
    
    ffiles = [os.path.join(import_dir, f) for f in files]
    #tofiles = [os.path.join(importpath, f[i1:-i2] + '.png') for f in files]
    tofiles = [conv_name(importpath, f, i1, i2) for f in files]
    
    fn = zip(ffiles, tofiles)
    
    for f, t in fn:
        print 'cp', f, t
        shutil.copy(f, t)

try:
    import_dir = sys.argv[1]
except IndexError, e:
    print "Usage: %s import_dir" % os.path.basename(sys.argv[0])
    sys.exit(1)

#importpath = 'data/newexp/segmented_image'
#do_stuff(import_dir, importpath, 41, -19)
importpath = 'data/newexp/projection'
do_stuff(import_dir, importpath, 16, -19)
