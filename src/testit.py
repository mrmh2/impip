#!/usr/bin/env python2.7

import os
import sys
import shutil

from mutil import mkdir_p

def ensure_tidy(test_data_path):
    shutil.rmtree(test_data_path)

def setup(input_path, test_data_path):

    ensure_tidy(test_data_path)

    mic_file_path = os.path.join(test_data_path, 'microscope_file')

    print "Creating directory:"
    print "   ", mic_file_path
    mkdir_p(mic_file_path)

    files = [f for f in os.listdir(input_path)]
    exts = [os.path.splitext(f)[1] for f in files]
    newnames = ['T%02d' % n + e for n, e in enumerate(exts)]
    sources = [os.path.join(input_path, f) for f in files]
    dests = [os.path.join(mic_file_path, f) for f in newnames]

    for s, d in zip(sources, dests):
        print "Copying:"
        print "   ", s
        print "into:"
        print "   ", d
        shutil.copy(s, d)


def main():
    input_path = 'unittest/raw_data'
    test_data_path = 'unittest/test_dataset'
    setup(input_path, test_data_path)

    #test_list_initial_files()

if __name__ == '__main__':
    main()
