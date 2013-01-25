#!/usr/bin/env python
import os
import sys
import subprocess
import shutil

from filter import get_binary_path, get_parfile_path

gencfile = "Output_CellShapeAnalysis/out/out.dat"

def process(input_filename, output_filename):
    print "Getting csa %s to %s" % (input_filename, output_filename)
    generate_csa(input_filename, output_filename)

def generate_csa(sf, lf):
    csacommand = get_binary_path('config/tools.cfg', 'gencsa')
    parfile = get_parfile_path('config/tools.cfg', 'gencsa')
 
    runcommand = [csacommand, parfile, "out", sf]

    #print "Generating %s" % lf
    p = subprocess.Popen(runcommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #TODO - Error handling
    so, se = p.communicate()

    #print se, so

    #print "From %s to %s" % (genlfile, lf)
    #shutil.copy(genlfile, lf)

    #with open(genlfile, 'r') as f:
    #    lines = [l.strip() for l in f.readlines()]

    #rawdata = [l for l in lines[2:] if l.find('sigma') == -1]
    #lnumbers = dict([(int(l.split()[0]), l.split()[1:]) for l in rawdata])

    #with open(lf, 'w') as f:
    #    for id in sorted(lnumbers):
    #        nicely = ['%10f' % float(lc) for lc in lnumbers[id][2:16]]
    #        f.write('%s: %s\n' % (id, ''.join(nicely)))
    shutil.copy(gencfile, lf)

def main():
    try:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
    except IndexError:
        print "Usage: %s input_filename output_filename" % os.path.basename(sys.argv[0])
        sys.exit(0)

    process(input_filename, output_filename)

if __name__ == '__main__':
    main()
