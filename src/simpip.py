#!/usr/bin/env python

# Define new pipeline with 4 data stages:
# Original images
# Segmented images
# L numbers

# stage1 = lif file
# stage2 = image stack
# stage3 = projection
# stage4 = segmented image
# stage5 = L numbers
# stage6 = tracking map

import stages
import pipeline


def generate_l_coeffs(of, sf, lf):
    runcommand = [lcommand, parfile, "tmp", of, sf, sf]

    print "Generating %s" % lf
    p = subprocess.Popen(runcommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #TODO - Error handling
    o, se = p.communicate()

    #print se, so

d1 = stages.DataStage("Microscope file")
d2 = stages.DataStage("Image stack")
d3 = stages.DataStage("Projection")
d4 = stages.DataStage("Segmented image")
d5 = stages.DataStage("L numbers")
#print md
#du2 = stages.DataUnit(d1)
#du2.set_filename("test.png")
du4 = stages.DataUnit(d4)
du4.set_filename("data/ex01/stage4/EditSegmentation2D_001343216175_ExpID3002_TL010_plantD_cropped.png")
p1 = stages.ProcessStage()
p1.command = None




