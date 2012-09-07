#!/usr/bin/env python

"""Reads lif files and parses metadata. Writes voxel spacing to a config file.
Usage:

parsemeta.py lif_file config_file
"""

import os
import sys
import pprint
import subprocess
import ConfigParser

def read_metadata(lines):

    splitl = [l.split(':') for l in lines]
    params = dict([p for p in splitl if len(p) > 1])

    return params

def trans(pval):
    return float(pval) * 1e6

def get_param_pairs(param_dict):

    param_list = [
        ['voxel size x', 'HardwareSetting|ScannerSettingRecord|dblVoxelX 0'],
        ['voxel size y', 'HardwareSetting|ScannerSettingRecord|dblVoxelY 0'],
        ['voxel size z', 'HardwareSetting|ScannerSettingRecord|dblVoxelZ 0']]

    return [(name, trans(param_dict[key])) for name, key in param_list]

def write_config(pps, output_file):

    config = ConfigParser.SafeConfigParser()
    
    sname = 'Microscope data'
    config.add_section(sname)

    for name, val in pps:
        config.set(sname, name, str(val))

    with open(output_file, 'wb') as f:
        config.write(f)

def generate_metadata(filename):
    showinf = '/storage/shared/tools/bftools/showinf'
    cmd = [
            showinf,
            '-nopix',
            filename]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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

if __name__ == '__main__':
    main()
