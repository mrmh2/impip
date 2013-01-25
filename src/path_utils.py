#!/usr/bin/env python

import os
import sys

def extract_int(substring):

    term_char = ['_', '.']

    ends = [substring.find(t) for t in term_char]
    filtered_ends = [e for e in ends if e != -1]
    end = min(filtered_ends)

    return int(substring[:end])

def parse_filename(filename):
    print filename

    chars = ['S', 'X', 'C', 'Z']

    return {c: extract_int(filename[1 + filename.find(c):]) for c in chars}

def get_file_selection(fds, s, t):
    fl = []

    for fd in fds:
        if fds[fd]['S'] == s and fds[fd]['X'] == t:
            fl.append(fd)

    return fl

def dirit(dirname):
    files = os.listdir(dirname)
    
    fds = {f: parse_filename(f) for f in files}

    file_root = files[0][:files[0].find('_X')]

    s_vals = set([fd['S'] for fd in fds.values()])

    fsplit_d = {}

    for s in s_vals:
        t_vals = set([fd['X'] for fd in fds.values() if fd['S'] == s])
        for t in t_vals:
            projection_name = '%s_S%02dX%02d' % (file_root, s, t)
            file_sel = get_file_selection(fds, s, t)

            fsplit_d[projection_name] = file_sel

    return fsplit_d

def main():
    fd = dirit(sys.argv[1])

    print fd

    for fn in fd:
        params = 2, 2, 1, 0
        proj_name = fn + '-proj.png'
        surf_name = fn + '-surf.png'

        file_paths = [os.path.join(sys.argv[1], f) for f in fd[fn]]

        projection_from_file_list(file_paths, proj_name, surf_name, params)
    #params = 8, 8, 6, 10
    #projection_from_file_list(sys.argv[1:], 'newproj.png', 'newsurf.png', params)

if __name__ == '__main__':
    main()


