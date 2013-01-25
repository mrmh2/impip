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
    pl.create_data_stage("Thresholded projection")
    pl.create_data_stage("Cleaned projection")
    pl.create_data_stage("Surface height map")
    pl.create_data_stage("Projection")
    pl.create_data_stage("Segmented image")
    pl.create_data_stage("New segmented image")
    pl.create_data_stage("False colour image")
    pl.create_data_stage("L numbers")
    pl.create_data_stage("CSA")

    pl.create_process_stage("Generate stack", 'mictostack', '')
    pl.create_process_stage("Create gaussian projection", "stacktoproj")
    pl.create_process_stage("Get L numbers", 'genlnumbers', '.txt')
    pl.create_process_stage("Get microscope metadata", 'getmicmeta')
    pl.create_process_stage("Thresholding", 'threshold')
    pl.create_process_stage("Segmentation", 'segment')
    pl.create_process_stage("Cell shape analysis", 'gencsa', '.txt')

    pl.connect_by_name("Segmented image", "Cell shape analysis", "CSA")
    pl.connect_by_name("Microscope file", "Get microscope metadata", "Microscope metadata")
    pl.connect_by_name("Microscope file", "Generate stack", "Image stack")
    pl.connect_by_name("Segmented image", "Get L numbers", "L numbers")
    pl.connect_by_name("Image stack", "Create gaussian projection", "Gaussian projection")
    pl.connect_by_name("Image stack", "Create gaussian projection", "Surface height map")
    #pl.connect_by_name("Thresholded projection", "Segmentation", "New segmented image")
    #pl.connect_by_name("Thresholded projection", "Segmentation", "False colour image")

    pl.connect_by_name("Gaussian projection", "Thresholding", "Thresholded projection")

    ps = pl.pstages["Create gaussian projection"]
    ps.output_map = ["Gaussian projection", "Surface height map"]

    #ps = pl.pstages["Segmentation"]
    #ps.output_map = ["New segmented image", "False colour image"]

    return pl
