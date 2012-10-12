#!/usr/bin/env python

import os
import sys
import shutil

from mutil import mkdir_p

def parse_stack_filename(fn):
    name, ext = os.path.splitext(fn)

    split = name.split('_')

    prefix = split[0]
    channel = split[1][1:]
    series = split[2][1:]
    z = split[3][1:]

    return prefix, channel, series, z

def split_stack(stack_path):
    files = [fn for fn in os.listdir(stack_path) if 
        os.path.isdir(os.path.join(stack_path, fn)) == False]
    ps = [parse_stack_filename(fn) for fn in files]

    unique_series = set([int(s) for p, c, s, z in ps])

    if len(unique_series) > 1:

        series_names = ['series%d' % s for s in unique_series]
        series_paths = [os.path.join(stack_path, n) for n in series_names]
        print series_paths

        for sp in series_paths:
            mkdir_p(sp)

        for s, sp in zip(unique_series, series_paths):
            sfiles = [fn for fn in os.listdir(stack_path) if fn.find('S%d' % s) != -1]
            sfrom = [os.path.join(stack_path, sf) for sf in sfiles]
            sto = [os.path.join(sp, sf) for sf in sfiles]
            for sf, st in zip(sfrom, sto):
                print sf, st
                shutil.move(sf, st)

    unique_channels = set([int(c) for p, c, s, z in ps])

    if len(unique_channels) > 1:
        channel_names = ['channel%d' % c for c in unique_channels]
        channel_paths = [os.path.join(stack_path, n) for n in channel_names]

        for cp in channel_paths:
            mkdir_p(cp)

        for c, cp in zip(unique_channels, channel_paths):
            cfiles = [fn for fn in os.listdir(stack_path) if fn.find('C%d' % c) != -1]
            cfrom = [os.path.join(stack_path, cf) for cf in cfiles]
            cto = [os.path.join(cp, cf) for cf in cfiles]
            for cf, ct in zip(cfrom, cto):
                print cf, ct
                shutil.move(cf, ct)


def main():
    try:
        input_path = sys.argv[1]
    except IndexError:
        print "ERROR: Please supply directory"
        sys.exit(0)

    split_stack(input_path)


if __name__ == '__main__':
    main()

