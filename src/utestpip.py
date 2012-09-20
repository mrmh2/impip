#!/usr/bin/env python

import pipeline

def create_pipeline():
    # Name
    pl = pipeline.Pipeline("Unit testing pipeline")
    
    # Data stages
    pl.create_data_stage("Microscope file")
    pl.create_data_stage("Microscope metadata")
    pl.create_data_stage("Image stack")
    pl.create_data_stage("Projection")
    pl.create_data_stage("Surface height map")
    pl.create_data_stage("Segmented image")
    pl.create_data_stage("False colour image")
    pl.create_data_stage("L numbers")

    pl.create_process_stage("Generate stack", 'mictostack', '')
    pl.create_process_stage("Get microscope metadata", 'getmicmeta', '.txt')
    pl.create_process_stage("Create gaussian projection", "stacktoproj")
    #pl.create_process_stage("Thresholding", 'threshold')
    pl.create_process_stage("Segmentation", 'segment')
    pl.create_process_stage("Get L numbers", 'lnumber', '.txt')

    pl.connect_by_name("Microscope file", "Get microscope metadata", "Microscope metadata")
    pl.connect_by_name("Microscope file", "Generate stack", "Image stack")
    pl.connect_by_name("Segmented image", "Get L numbers", "L numbers")
    pl.connect_by_name("Image stack", "Create gaussian projection", "Projection")
    pl.connect_by_name("Image stack", "Create gaussian projection", "Surface height map")
    pl.connect_by_name("Projection", "Segmentation", "Segmented image")
    pl.connect_by_name("Projection", "Segmentation", "False colour image")

    #pl.connect_by_name("Gaussian projection", "Thresholding", "Thresholded projection")

    ps = pl.pstages["Create gaussian projection"]
    ps.output_map = ["Projection", "Surface height map"]

    ps = pl.pstages["Segmentation"]
    ps.output_map = ["Segmented image", "False colour image"]

    return pl
