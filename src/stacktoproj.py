#!/usr/bin/env python
"""stacktoproj.py

This module acts both as part of an image processing pipeline, or a standalone
executable. If run as a standalone executable, it should be called as:

stacktoproj.py input_directory output_file

It will convert a stack of PNGs in the input directory into a projection in the
output_directory."""

import os
import sys
import errno
import shutil
import subprocess

gaussproj = '/storage/shared/tools/gaussproj/gaussproj.py'

def process(input_path, output_filename):

    tmpdir = '/tmp/stackproj'
    output_file = 'proj-g3d-8-8-6-10.png'
    make_dir_if_needed(tmpdir)
    #basename = os.path.basename(output_path)
    #fullname = "%s_C%%c_S%%s_Z%%z.png" % basename
    #fullpath = os.path.join(output_path, fullname)
    #print fullpath

    cmd = [
            gaussproj,
            input_path,
            tmpdir]

    subprocess.call(cmd)

    output_name = os.path.join(tmpdir, output_file)
    shutil.copy(output_name, output_filename)

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
