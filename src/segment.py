#!/usr/bin/env python
"""segment.py

Wrapper around SPM segmentation program to turn it into an image filter for pipeline use.
At present, keeps only the cell state and throws away the false colour image.

Usage:

segment.py input_file output_segmentation output_falsecolor
"""

import os
import sys
import errno
import shutil
import tempfile
import subprocess

home = os.environ['HOME']
scommand = os.path.join(home, 'tools/bin/spm2D_1_0_0')
parfile = os.path.join(home, 'tools/par/spm2d.par')

def find_output_file(path, od):

    of = '00000.png'
    outpath = [dp for dp, dns, fns in os.walk(path) if dp.find(od) != -1]

    return os.path.join(outpath[0], of)

def process(input_filenames, output_filenames):
    print "segment.process() called with", input_filenames, output_filenames
    segment_image(input_filenames[0], output_filenames[0], output_filenames[1])

def segment_image(input_file, dest_seg, dest_col):

    temp_path = tempfile.mkdtemp()
    
    runcommand = [  scommand,
                    temp_path,
                    parfile,
                    input_file]

    p = subprocess.Popen(runcommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #TODO - Error handling
    stdout, stderr = p.communicate()

    out_seg = find_output_file(temp_path, 'CellstateFinal')
    out_col = find_output_file(temp_path, 'Cellcolors')

    try:
        shutil.copy(out_seg, dest_seg)
        shutil.copy(out_col, dest_col)
    except IOError, e:
        if e.errno == errno.ENOENT:
            print "Segmentation failed"
            print stdout, stderr
            
def main():
    try:
        input_filename = sys.argv[1]
        output_seg = sys.argv[2]
        output_colour = sys.argv[3]
    except IndexError:
        print __doc__
        sys.exit(2)
        
    process([input_filename], [output_seg, output_colour])

if __name__ == '__main__':
    main()
