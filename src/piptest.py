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

    # Processing stages
    pl.create_process_stage("Rotate 90 ccw", 'rotate')
    pl.create_process_stage("Get PNG data", 'pngdata', '.txt')

    # Connections
    pl.connect_by_name("Raw image", "Rotate 90 ccw", "Rotated image")
    pl.connect_by_name("Raw image", "Get PNG data", "PNG data on raw image")

    return pl
