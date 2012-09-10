#!/usr/bin/env python2.7
"""
pgvplot

Plots pipelines using pygraphviz as png. Usage:

pgvplot.py pipeline_name output_filename
"""

import os
import sys

import pygraphviz as pgv

def load_pipeline_by_name(plname):

    pline = __import__(plname)
    pl = pline.create_pipeline()
    return pl
    

def plot_pipeline(plname, output_file):
    pl = load_pipeline_by_name(plname)
    
    G = pgv.AGraph(directed=True)
    
    for dname in pl.dstages:
        G.add_node(dname, shape='box', color='blue')
    
    for pname in pl.pstages:
        G.add_node(pname, shape='ellipse', color='red')
    
    for f, p, t in pl.connections:
        G.add_edge((f, p))
        G.add_edge((p, t))
    
    print G
    
    G.layout(prog='dot')

    G.draw(output_file)

def main():
    try:
       plname = sys.argv[1]
       output_file = sys.argv[2]
    except IndexError:
        print __doc__
        sys.exit(2)

    plot_pipeline(plname, output_file)

if __name__ == '__main__':
    main()
