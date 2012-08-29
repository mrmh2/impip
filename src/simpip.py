#!/usr/bin/env python

# Define new pipeline with some data stages
# Original images
# Segmented images
# L numbers

# stage1 = lif file
# stage2 = image stack
# stage3 = projection
# stage4 = segmented image
# stage5 = L numbers
# stage6 = tracking map

import pipeline

def create_pipeline():
    pl = pipeline.Pipeline("Pavement cells")
    
    #d1 = pipeline.DataStage("Microscope file")
    #pl.add_data_stage(d1)
    
    #d2 = pipeline.DataStage("Image stack")
    #pl.add_data_stage(d2)
    #
    d3 = pipeline.DataStage("Projection")
    pl.add_data_stage(d3)

    d34 = pipeline.DataStage("Rotated projection")
    pl.add_data_stage(d34)
    #
    d4 = pipeline.DataStage("Segmented image")
    pl.add_data_stage(d4)
    #
    d5 = pipeline.DataStage("Rotated image")
    pl.add_data_stage(d5)
    
    d6 = pipeline.DataStage("L numbers")
    pl.add_data_stage(d6)
    
    p1 = pipeline.ProcessStage("Rotate 90 ccw", 'rotate')
    pl.add_processing_stage(p1)
    pl.connect(d4, p1, d5)

    p2 = pipeline.ProcessStage("Rotate projection 90 ccw", 'rotate')
    pl.add_processing_stage(p2)
    pl.connect(d3, p2, d34)

    p3 = pipeline.ProcessStage("Get L numbers", 'lnumber')
    p3.ext = 'txt'
    pl.add_processing_stage(p3)
    pl.connect(d5, p3, d6)

    return pl
