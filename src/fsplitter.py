#!/usr/bin/env python

def process(input_filenames, output_filenames):
    in_file = input_filenames[0]

    with open(in_file, "r") as f:
        data = f.readlines()

    for n, fname in enumerate(output_filenames):
        with open(fname, "w") as f:
            lines = ["Copy %d: %s" % (n, l) for l in data]
            for l in lines:
                f.write(l)
