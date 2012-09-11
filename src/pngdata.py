#!/usr/bin/env python

import sys
import errno
import subprocess

def process(input_filename, output_filename):
    toolname = 'exiftool'
    cmd = [
            toolname,
            input_filename]

    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    except OSError, e:
        if e.errno == errno.ENOENT:
            print "ERROR: %s not found on path" % toolname
            sys.exit(2)
        else: raise

    stdout, stderr = p.communicate()

    with open(output_filename, 'w') as f:
        f.write(stdout)
