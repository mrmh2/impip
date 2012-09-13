#!/usr/bin/env python
"""filter.py 

Base image filter class for use in pipelines. Derived classes should override the process method.
"""
import os
import sys
import shutil
import subprocess

class Filter(object):
    def __init__(self):
        pass

    def process(input_files, output_files):
        print "Base method - you must override me!"
        sys.exit(2)

    def main():
        

home = os.environ['HOME']
scommand = os.path.join(home, 'tools/bin/spm2D_1_0_0')
parfile = os.path.join(home, 'tools/par/spm2d.par')

def process(input_filename, output_filename):
    segment_image(input_file, output_file)

def segment_image(input_file, output_file):

    sys.exit(0)
    runcommand = []

    print "Generating %s" % lf
    p = subprocess.Popen(runcommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #TODO - Error handling
    o, se = p.communicate()

    #print se, so

    #print "From %s to %s" % (genlfile, lf)
    shutil.copy(genlfile, lf)
 

def main():
    try:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
    except IndexError:
        print __doc__
        sys.exit(2)
        
    process(input_filename, output_filename)

if __name__ == '__main__':
    main()
