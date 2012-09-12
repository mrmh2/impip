#!/usr/bin/env python2.7

import os
import sys
import shutil

from mutil import mkdir_p

def setup():
    input_path = 'test/images'
    test_data_path = 'data/unittest/raw_image'

    mkdir_p(test_data_path)

    files = [f for f in os.listdir(input_path)]
    sources = [os.path.join(input_path, f) for f in files]
    dests = [os.path.join(test_data_path, f) for f in files]

    for s, d in zip(sources, dests):
        shutil.copy(s, d)


def main():
    setup()

    #test_list_initial_files()

if __name__ == '__main__':
    main()
