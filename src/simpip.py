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

filename = "data/ex01/stage4/EditSegmentation2D_001343216175_ExpID3002_TL010_plantD_cropped.png"

pl = pipeline.Pipeline("Pavement cells")

#d1 = pipeline.DataStage("Microscope file")
#pl.add_data_stage(d1)

#d2 = pipeline.DataStage("Image stack")
#pl.add_data_stage(d2)
#
#d3 = pipeline.DataStage("Projection")
#pl.add_data_stage(d3)
#
d4 = pipeline.DataStage("Segmented image")
pl.add_data_stage(d4)
#
d5 = pipeline.DataStage("Rotated image")
pl.add_data_stage(d5)

d6 = pipeline.DataStage("L numbers")

p1 = pipeline.ProcessStage("Rotate 90 ccw")
pl.add_processing_stage(p1)

pl.connect(d4, p1, d5)

#du4 = pipeline.DataUnit(d4)
#du4.set_filename("data/ex01/stage4/EditSegmentation2D_001343216175_ExpID3002_TL010_plantD_cropped.png")

#pl.add_data_unit(du4)

dt = pipeline.DataTrack("T003", pl)
dt.import_file(filename, d4)


print pl

pl.run(dt)
