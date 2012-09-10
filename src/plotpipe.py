#!/usr/bin/env python2.7

from pygraph.classes.digraph import digraph
from pygraph.readwrite.dot import write

import pygraphviz as pgv

plname = "fullpip"

pline = __import__(plname)

gr = digraph()
pl = pline.create_pipeline()

def simple():
    for dname in pl.dstages:
        gr.add_nodes([dname])
    
    for f, label, t in pl.connections:
        gr.add_edge((f, t), label=label)

#for dname in pl.dstages:
#    gr.add_nodes([dname])
gr.add_nodes(pl.dstages.keys())
gr.add_nodes(pl.pstages.keys())

#for pname in pl.pstages:
#    gr.add_nodes([pname])

trackit = []
    
for f, p, t in pl.connections:
    if f + p not in trackit:
        gr.add_edge((f, p))
        trackit.append(f + p)
    if p + t not in trackit:
        gr.add_edge((p, t))
        trackit.append(p + t)

dot = write(gr)

print dot

G = pgv.AGraph(dot)

G.layout(prog='dot')

G.draw('pg.png')
