#!/usr/bin/env python
"""stacktoproj.py

This module acts both as part of an image processing pipeline, or a standalone
executable. If run as a standalone executable, it should be called as:

stacktoproj.py input_directory output_file surface_file

It will convert a stack of PNGs in the input directory into a projection as the
output_file and a surface file."""

import os
import sys
import errno
import shutil
import tempfile
import subprocess

from filter import get_binary_path
from path_utils import dirit
from gaussproj import projection_from_file_list

#gaussproj = '/storage/shared/tools/gaussproj/gaussproj.py'

def single_projection(input_path, projection_file, surface_file):

    print "I got called to turn %s into projection %s and surface %s" % (input_path, 
        projection_file, surface_file)


    tmpdir = tempfile.mkdtemp()
    gaussproj = get_binary_path('config/tools.cfg', 'stacktoproj')
    output_projection = 'proj-g3d-3-3-2-10.png'
    output_surface = 'surface-g3d-3-3-2-10.png'
    cmd = [
            gaussproj,
            input_path,
            tmpdir]

    try:
        subprocess.call(cmd)
    except OSError, e:
        if e.errno == errno.ENOENT:
            print "ERROR: Binary command %s not found" % gaussproj
            sys.exit(2)
        else: raise

    output_name = os.path.join(tmpdir, output_projection)
    shutil.copy(output_name, projection_file)

    output_name = os.path.join(tmpdir, output_surface)
    shutil.copy(output_name, surface_file)

def mod_filename(filename, char, i):
    #print filename
    #path, name = os.path.split(filename)
    #print path, name
    base, ext = os.path.splitext(filename)
    return base + '-' + char + str(i) + ext


def process(input_paths, output_filenames):

    input_path = input_paths[0]

    tmpdir = tempfile.mkdtemp()
    #make_dir_if_needed(tmpdir)

    fds = dirit(input_path)
    proj_path = os.path.split(output_filenames[0])[0]
    surf_path = os.path.split(output_filenames[1])[0]

    for fn in fds:
        proj_file = os.path.join(proj_path, fn) + '.png'
        surf_file = os.path.join(surf_path, fn) + '.png'

        params = 3, 3, 2, 0

        file_list = [os.path.join(input_path, f) for f in fds[fn]]

        projection_from_file_list(file_list, proj_file, surf_file, params)

    sys.exit(0)
        #single_projection(


    subdirs = [d for d in os.listdir(input_path) if 
        os.path.isdir(os.path.join(input_path, d))]

    if not len(subdirs):
    # Simple stack with no channels/series
        projection_file = output_filenames[0]
        surface_file = output_filenames[1]
        print "I got called to turn %s into projection %s and surface %s" % (input_path, 
            projection_file, surface_file)
        single_projection(input_path, projection_file, surface_file)
    else:
        input_paths = [os.path.join(input_path, d) for d in subdirs]
        for n, ip in enumerate(input_paths):
            pf = mod_filename(output_filenames[0], 's', n)
            of = mod_filename(output_filenames[1], 's', n)
            single_projection(ip, pf, of)

def make_dir_if_needed(dirname):
    try:
        os.makedirs(dirname)
    except OSError, e:
        if e.errno == errno.EEXIST:
            pass
        else: raise

    try:
        os.listdir(dirname)
    except OSError, e:
        if e.errno == errno.ENOTDIR:
            print "%s exists but is not a directory" % dirname
            sys.exit(2)
        else: raise

def main():
    try:
        input_path = sys.argv[1]
        output_filenames = sys.argv[2:4]
    except IndexError:
        print __doc__
        sys.exit(0)

    process([input_path], output_filenames)


if __name__ == '__main__':
    main()
