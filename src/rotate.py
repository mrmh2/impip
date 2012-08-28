#!/usr/bin/env python

import subprocess

def process(input_filename, output_filename):
    cmd = [
            'convert',
            '-rotate',
            '270',
            input_filename,
            output_filename]
    subprocess.call(cmd)
