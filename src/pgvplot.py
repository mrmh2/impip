#!/usr/bin/env python2.7

import pygraphviz as pgv

plname = "fullpip"
pline = __import__(plname)

pl = pline.create_pipeline()

G = pgv.AGraph(directed=True)

G.get_node(

for dname in pl.dstages:
    G.add_node(dname, shape='box', color='blue')

for pname in pl.pstages:
    G.add_node(pname, shape='ellipse', color='red')

for f, p, t in pl.connections:
    G.add_edge((f, p))
    G.add_edge((p, t))

#    gr.add_nodes([dname])

print G

G.layout(prog='dot')
G.draw("mygraph.png")




