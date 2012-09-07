#!/usr/bin/env python

import os, sys, shutil
import pprint
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
        #shutil.copy(f, t)

def has_text(text):
    def my_filter(f):
        if f.find(text) != -1: return True
        else: return False

    return my_filter

def make_names(dirpath, filenames):
    return [os.path.join(dirpath, name) for name in filenames]

def list_dir_recursive(import_from):
    files = [make_names(dp, fns) for dp, dns, fns in os.walk(import_from)]
    files_flat = sum(files, [])
    return files_flat

def generate_destination_names(destdir, f):
    tl = f.find("TL")
    tp = int(f[tl+2:tl+5]) - 1
    fname = "T%02d.lif" % tp
    return os.path.join(destdir, fname)

def main():
    try:
        import_from = sys.argv[1]
        import_dest = sys.argv[2]
    except IndexError, e:
        print "Usage: %s import_from import_dest" % os.path.basename(sys.argv[0])
        sys.exit(1)
    
    
    files_flat = list_dir_recursive(import_from)
    selected_files = filter(has_text('plantD'), files_flat)
    destinations = [generate_destination_names(import_dest, f) for f in selected_files]

    for f, t in zip(selected_files, destinations):
        print "cp %s %s" % (f, t)
        shutil.copy(f, t)

if __name__ == '__main__':
    main()
    

#importpath = 'data/newexp/segmented_image'
#do_stuff_n(import_dir, importpath)

#importpath = 'data/oldexp/rotated_image'
#do_stuff_n(import_dir, importpath)

#importpath = 'data/oldexp/rotated_projection'
#do_stuff_n(import_dir, importpath)
