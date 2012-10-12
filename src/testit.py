#!/usr/bin/env python2.7

import os
import sys
import shutil

from mutil import mkdir_p

def setup():
    input_path = 'test/lif'
    test_data_path = 'data/unittest/microscope_file/'

    print "Creating directory:"
    print "   ", test_data_path
    mkdir_p(test_data_path)

    files = [f for f in os.listdir(input_path)]
    exts = [os.path.splitext(f)[1] for f in files]
    newnames = ['T%02d' % n + e for n, e in enumerate(exts)]
    sources = [os.path.join(input_path, f) for f in files]
    dests = [os.path.join(test_data_path, f) for f in newnames]

    for s, d in zip(sources, dests):
        print "Copying:"
        print "   ", s
        print "into:"
        print "   ", d
        shutil.copy(s, d)


def main():
    setup()

    #test_list_initial_files()

if __name__ == '__main__':
    main()
