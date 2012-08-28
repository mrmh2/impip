#!/usr/bin/env python

import os, sys, shutil

try:
    import_dir = sys.argv[1]
except IndexError, e:
    print "Usage: %s import_dir" % os.path.basename(sys.argv[0])

importpath = 'data/newexp/segmented_image'

files = os.listdir(import_dir)
ffiles = [os.path.join(import_dir, f) for f in files]
tofiles = [os.path.join(importpath, f[42:-19] + '.png') for f in files]

fn = zip(ffiles, tofiles)

for f, t in fn:
    print 'cp', f, t
    shutil.copy(f, t)
