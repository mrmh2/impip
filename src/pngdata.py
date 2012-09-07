#!/usr/bin/env python

import subprocess

def process(input_filename, output_filename):
    toolname = 'exiftool'
    cmd = [
            toolname,
            input_filename]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    stdout, stderr = p.communicate()

    with open(output_filename, 'w') as f:
        f.write(stdout)
