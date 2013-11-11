#!/usr/bin/env python

"""Reads lif files and parses metadata. Writes voxel spacing to a config file.
Usage:

parsemeta.py lif_file config_file
"""

import os
import sys
import errno
import pprint
import subprocess
import ConfigParser

def get_binary_path(cfile):
    if not os.path.exists(cfile):
        print "ERROR: Config file %s missing" % cfile
        sys.exit(2)

    config = ConfigParser.SafeConfigParser()
    config.read(cfile)
    sname = 'getmicmeta'
    
    try:
        result = config.get(sname, 'bin')
    except ConfigParser.NoSectionError:
        print "ERROR: Couldn't open %s, or section %s was missing" % (cfile, sname)
        sys.exit(2)

    return result.replace("'", "")

def read_metadata(lines):
    splitl = [l.split(':') for l in lines]
    params = dict([p for p in splitl if len(p) > 1])

    return params

def trans_zeiss(pval):
    return float(pval) * 1e6

def trans_leica(pval):
    return float(pval)

def get_param_pairs(param_dict):


    param_list = [
        ['voxel size x', 'HardwareSetting|ScannerSettingRecord|dblVoxelX 0'],
        ['voxel size y', 'HardwareSetting|ScannerSettingRecord|dblVoxelY 0'],
        ['voxel size z', 'HardwareSetting|ScannerSettingRecord|dblVoxelZ 0'],
        ['x position', 'HardwareSetting|FilterSettingRecord|DM6000 Stage Pos x 0'],
        ['y position', 'HardwareSetting|FilterSettingRecord|DM6000 Stage Pos y 0']]


    try:
        param_dict = [(name, trans_zeiss(param_dict[key])) for name, key in param_list]
    except KeyError:
        # If we don't have those values, this is not Zeiss metadata
        param_list = [
            ['voxel size x', 'VoxelSizeX'],
            ['voxel size y', 'VoxelSizeY'],
            ['voxel size z', 'VoxelSizeZ']]
        param_dict = [(name, trans_leica(param_dict[key])) for name, key in param_list]
    
    return param_dict

def write_config(pps, output_file):

    config = ConfigParser.SafeConfigParser()
    
    sname = 'Microscope data'
    config.add_section(sname)

    for name, val in pps:
        config.set(sname, name, str(val))

    with open(output_file, 'wb') as f:
        config.write(f)

def generate_metadata(filename):
    #showinf = '/storage/shared/tools/bftools/showinf'
    showinf = get_binary_path('config/tools.cfg')
    #showinf2 = '/Users/hartleym/packages/bftools/showinf'
    #print showinf, showinf2
    #print type(showinf), type(showinf2)

    #sys.exit(0)
    cmd = [
            showinf,
            '-nopix',
            filename]

    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError, e:
        if e.errno == errno.ENOENT:
            print "ERROR: Couldn't open tool binary %s" % cmd
            sys.exit(2)
        else: raise

    stdout, stderr = p.communicate()

    return stdout.split('\n')

def process(input_file, output_file):
    rawmeta = generate_metadata(input_file)
    param_dict = read_metadata(rawmeta)
    pps = get_param_pairs(param_dict)
    write_config(pps, output_file)

def main():
    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    except IndexError:
        print __doc__
        sys.exit(2)

    process(input_file, output_file)

if __name__ == '__main__':
    main()
