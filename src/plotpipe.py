#!/usr/bin/env python2.7
"""
plotpipe.py

Produces a PNG plot of the specified pipeline. Usage:

plotpipe.py pipeline_name output_filename
"""

import os
import sys

from pygraph.classes.digraph import digraph
from pygraph.readwrite.dot import write
import pygraphviz as pgv

from pltools import load_pipeline_by_name

#def load_pipeline_by_name(plname):
#    pline = __import__(plname)
#    return pline.create_pipeline()

def pygraph_build_pipeline_graph(pl):
    gr = digraph()

    gr.add_nodes(pl.dstages.keys())
    gr.add_nodes(pl.pstages.keys())

    unique_inputs = set([(f, p) for f, p, _ in pl.connections])
    unique_outputs = set([(p, t) for _, p, t in pl.connections])
    [gr.add_edge(i) for i in unique_inputs | unique_outputs]

    return gr


def prettify_graph(pl, G):
    dnodes = [G.get_node(name) for name in pl.dstages]

    for n in dnodes:
        n.attr['shape'] = 'box'
        n.attr['color'] = 'blue'

    pnodes = [G.get_node(name) for name in pl.pstages]

    for n in pnodes:
        n.attr['shape'] = 'ellipse'
        n.attr['color'] = 'red'

def draw_pretty(pl, output_filename):
    gr = pygraph_build_pipeline_graph(pl)
    dot = write(gr)

    G = pgv.AGraph(dot, name=pl.name)
    prettify_graph(pl, G)
    G.layout(prog='dot')
    G.draw(output_filename)


def main():
    try:
       pipeline_name = sys.argv[1]
       output_filename = sys.argv[2]
    except IndexError:
        print __doc__
        sys.exit(2)

    pl = load_pipeline_by_name(pipeline_name)

    draw_prety(pl, output_filename)

if __name__ == '__main__':
    main()
