#!/usr/bin/env python

import pipeline
import simpip


pl = simpip.create_pipeline()

filename = "data/ex01/stage4/EditSegmentation2D_001343216175_ExpID3002_TL010_plantD_cropped.png"
dt1 = pipeline.DataTrack("T010", pl)
dt1.import_file(filename, "Segmented image")

fn2 = "/Users/hartleym/Projects/celltracking/data/ExpID3002/PlantD/Segmented_Images/EditSegmentation2D_001341593368_ExpID3002_TL001_plantD_cropped.png"
dt2 = pipeline.DataTrack("T001", pl)
dt2.import_file(fn2, "Segmented image")



print pl

pl.run(dt1)
pl.run(dt2)
