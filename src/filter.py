#!/usr/bin/env python
"""filter.py 

Base image filter class for use in pipelines. Derived classes should override the process method.
"""
import os
import sys
import shutil
import subprocess
import ConfigParser

def get_binary_path(cfile, sname):

    cfiles = [cfile]

    base, current = os.path.split(os.getcwd())
    cfiles.append(os.path.join(base, 'config/tools.cfg'))

    base, current = os.path.split(sys.argv[0])
    up = os.path.split(base)[0]
    cfiles.append(os.path.join(up, 'config/tools.cfg'))
    cfiles.append(os.path.join('/common/tools/impip', 'config/tools.cfg'))

    print cfiles

    cfexists = [os.path.exists(cf) for cf in cfiles]

    if not any(cfexists):
        print "ERROR: Config file %s missing" % cfiles
        sys.exit(2)

    config = ConfigParser.SafeConfigParser()
    config.read(cfiles)

    try:
        result = config.get(sname, 'bin')
    except ConfigParser.NoSectionError:
        print "ERROR: Couldn't open %s, or section %s was missing" % (cfile, sname)
        sys.exit(2)

    return result.replace("'", "")

def get_parfile_path(cfile, sname):
    if not os.path.exists(cfile):
        print "ERROR: Config file %s missing" % cfile
        sys.exit(2)

    config = ConfigParser.SafeConfigParser()
    config.read(cfile)
    #sname = __name__
    
    try:
        result = config.get(sname, 'par')
    except ConfigParser.NoSectionError:
        print "ERROR: Couldn't open %s, or section %s was missing" % (cfile, sname)
        sys.exit(2)

    return result.replace("'", "")



class Filter(object):
    def __init__(self):
        pass

    def process(input_files, output_files):
        print "Base method - you must override me!"
        sys.exit(2)

    def main():
        pass
        
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
