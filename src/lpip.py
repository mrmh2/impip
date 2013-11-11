#!/usr/bin/env python

# Define new pipeline with some data stages
# Original images
# Segmented correcteds
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
    
    pl.create_data_stage("Segmented corrected")
    pl.create_data_stage("L numbers")

    pl.create_process_stage("Get L numbers", 'genlnumbers', '.txt')

    pl.connect_by_name("Segmented corrected", "Get L numbers", "L numbers")

    return pl
