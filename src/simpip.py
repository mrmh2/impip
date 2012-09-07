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
    pl.create_data_stage("Image stack")
    pl.create_data_stage("Gaussian projection")
    pl.create_data_stage("Projection")
    pl.create_data_stage("Rotated projection")
    pl.create_data_stage("Segmented image")
    pl.create_data_stage("Rotated image")
    pl.create_data_stage("L numbers")

    pl.create_process_stage("Generate stack", 'mictostack', '')
    pl.create_process_stage("Gaussian projection", "stacktoproj")
    pl.create_process_stage("Rotate 90 ccw", 'rotate')
    pl.create_process_stage("Rotate projection 90 ccw", 'rotate')
    pl.create_process_stage("Get L numbers", 'lnumber', '.txt')
    pl.create_process_stage("Get microscope metadata", 'getmicmeta')

    pl.connect_by_name("Microscope file", "Get microscope metadata", "Microscope metadata")
    pl.connect_by_name("Microscope file", "Generate stack", "Image stack")
    pl.connect_by_name("Image stack", "Gaussian projection", "Gaussian projection")
    pl.connect_by_name("Segmented image", "Get L numbers", "L numbers")

    return pl
