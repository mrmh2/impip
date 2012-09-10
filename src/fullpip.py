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
    pl.create_data_stage("Projection")
    pl.create_data_stage("Surface height map")
    #pl.create_data_stage("Projection")
    pl.create_data_stage("Rotated projection")
    pl.create_data_stage("Segmented image")
    pl.create_data_stage("Rotated image")
    pl.create_data_stage("L numbers")
    pl.create_data_stage("Cell lineages")
    pl.create_data_stage("Cell measurements")

    pl.create_process_stage("Generate stack", 'mictostack', '')
    pl.create_process_stage("Gaussian projection", "stacktoproj")
    pl.create_process_stage("Rotate 90 ccw", 'rotate')
    pl.create_process_stage("Rotate projection 90 ccw", 'rotate')
    pl.create_process_stage("Get L numbers", 'lnumber', '.txt')
    pl.create_process_stage("Get microscope metadata", 'getmicmeta')
    pl.create_process_stage("Segmentation", 'segmentation')
    pl.create_process_stage("Cell tracking", 'tracker')
    pl.create_process_stage("Measure cells", 'measurer')

    pl.connect_by_name("Microscope file", "Get microscope metadata", "Microscope metadata")
    pl.connect_by_name("Microscope file", "Generate stack", "Image stack")
    pl.connect_by_name("Segmented image", "Get L numbers", "L numbers")
    pl.connect_by_name("Segmented image", "Rotate 90 ccw", "Rotated image")
    pl.connect_by_name("Image stack", "Gaussian projection", "Projection")
    pl.connect_by_name("Projection", "Rotate projection 90 ccw", "Rotated projection")
    pl.connect_by_name("Image stack", "Gaussian projection", "Surface height map")
    pl.connect_by_name("Projection", "Segmentation", "Segmented image")
    pl.connect_by_name("Rotated image", "Cell tracking", "Cell lineages")
    pl.connect_by_name("Rotated projection", "Cell tracking", "Cell lineages")
    pl.connect_by_name("L numbers", "Cell tracking", "Cell lineages")
    pl.connect_by_name("Projection", "Measure cells", "Cell measurements")
    pl.connect_by_name("Surface height map", "Measure cells", "Cell measurements")
    pl.connect_by_name("Microscope metadata", "Measure cells", "Cell measurements")

    ps = pl.pstages["Gaussian projection"]
    pl.output_map = ["Gaussian projection", "Surface height map"]

    return pl
