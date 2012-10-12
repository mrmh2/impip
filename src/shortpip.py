#!/usr/bin/env python

import pipeline

def create_pipeline():
    # Name
    pl = pipeline.Pipeline("Projection only pipline")
    
    # Data stages
    pl.create_data_stage("Microscope file")
    pl.create_data_stage("Microscope metadata")
    pl.create_data_stage("Image stack")
    pl.create_data_stage("Projection")
    pl.create_data_stage("Surface height map")
    pl.create_data_stage("Thresholded projection")

    pl.create_process_stage("Generate stack", 'mictostack', '')
    pl.create_process_stage("Get microscope metadata", 'getmicmeta', '.txt')
    pl.create_process_stage("Create gaussian projection", "stacktoproj")
    pl.create_process_stage("Thresholding", 'threshold')

    pl.connect_by_name("Microscope file", "Get microscope metadata", "Microscope metadata")
    pl.connect_by_name("Microscope file", "Generate stack", "Image stack")
    pl.connect_by_name("Image stack", "Create gaussian projection", "Projection")
    pl.connect_by_name("Image stack", "Create gaussian projection", "Surface height map")
    pl.connect_by_name("Projection", "Thresholding", "Thresholded projection")

    #pl.connect_by_name("Gaussian projection", "Thresholding", "Thresholded projection")

    ps = pl.pstages["Create gaussian projection"]
    ps.output_map = ["Projection", "Surface height map"]

    return pl
