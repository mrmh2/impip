#!/usr/bin/env python
"""mictostack.py

This module acts both as part of an image processing pipeline, or a standalone
executable. If run as a standalone executable, it should be called as:

mictostack.py input_filename output_directory

It will convert the microscope file input_filename to a stack in the directory
output_directory. It's a simple wrapper around Bioformats tool bfconvert."""

import os
import sys
import errno
import subprocess

bfconvert = '/usr/users/cbu/hartleym/packages/bftools/bfconvert'

def process(input_filename, output_path):

    make_dir_if_needed(output_path)
    basename = os.path.basename(output_path)
    fullname = "%s_C%%c_S%%s_Z%%z.png" % basename
    fullpath = os.path.join(output_path, fullname)
    print fullpath

    cmd = [
            bfconvert,
            input_filename,
            fullpath]

    subprocess.call(cmd)

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
        input_filename = sys.argv[1]
        output_path = sys.argv[2]
    except IndexError:
        print __doc__
        sys.exit(0)

    process(input_filename, output_path)


if __name__ == '__main__':
    main()
