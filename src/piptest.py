#!/usr/bin/env python

import pipeline

def create_pipeline():
    # Name
    pl = pipeline.Pipeline("Testing pipeline")
    
    # Data stages
    pl.create_data_stage("Raw image")
    pl.create_data_stage("Rotated image")
    pl.create_data_stage("PNG data")
    pl.create_data_stage("PNG data on raw image")
    pl.create_data_stage("Some text")
    pl.create_data_stage("More text")

    # Processing stages
    pl.create_process_stage("Rotate 90 ccw", 'rotate')
    pl.create_process_stage("Get PNG data", 'pngdata', '.txt')
    pl.create_process_stage("Split text", 'fsplitter', '.txt')

    # Connections
    pl.connect_by_name("Raw image", "Rotate 90 ccw", "Rotated image")
    pl.connect_by_name("Raw image", "Get PNG data", "PNG data on raw image")

    pl.connect_by_name("PNG data on raw image", "Split text", "Some text")
    pl.connect_by_name("PNG data on raw image", "Split text", "More text")

    ps = pl.pstages["Split text"]

    ps.output_map = ["Some text", "More text"]
    #ps.output_map = ["More text", "Some text"]

    return pl
