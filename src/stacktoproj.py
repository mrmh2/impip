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
import subprocess

from filter import get_binary_path

#gaussproj = '/storage/shared/tools/gaussproj/gaussproj.py'

def process(input_paths, output_filenames):

    input_path = input_paths[0]

    tmpdir = '/tmp/stackproj'
    output_projection = 'proj-g3d-8-8-6-10.png'
    output_surface = 'surface-g3d-8-8-6-10.png'
    make_dir_if_needed(tmpdir)

    projection_file = output_filenames[0]
    surface_file = output_filenames[1]

    print "I got called to turn %s into projection %s and surface %s" % (input_path, 
        projection_file, surface_file)

    gaussproj = get_binary_path('config/tools.cfg', __name__)

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
        output_filename = sys.argv[2]
    except IndexError:
        print __doc__
        sys.exit(0)

    process(input_path, output_filename)


if __name__ == '__main__':
    main()
