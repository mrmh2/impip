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
    
    pl.create_data_stage("Microscope file")
    pl.create_data_stage("Microscope metadata")

    pl.create_process_stage("Get microscope metadata", 'getmicmeta')

    pl.connect_by_name("Microscope file", "Get microscope metadata", "Microscope metadata")

    return pl
