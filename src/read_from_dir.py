#!/usr/bin/env python

import simpip
import pipeline
import os

pl = simpip.create_pipeline()

data_dir = 'data/newexp'

#dirs = [os.path.join(data_dir, pipeline.squash_name(ds)) for ds in pl.dstages]
#
#for d in dirs:
#    print os.listdir(d)
#
## TODO - make is a uniin
#for f in os.listdir(dirs[0]):
#    print ds[0], dirs[0], f

def get_prefix(f):
    p, e = os.path.splitext(f)
    return p

dts = {}
for ds_name in pl.dstages:
    ds_path = os.path.join(data_dir, pipeline.squash_name(ds_name))
    try:
        for f in os.listdir(ds_path):
            print ds_name, ds_path, f
            dt_name = get_prefix(f)
            if dt_name not in dts:
                print "Creating %s" % dt_name
                dts[dt_name] = pipeline.DataTrack(dt_name, pl)
            ds = pl.dstages[ds_name]
            du = pipeline.DataUnit(ds)
            du.set_filename(os.path.join(ds_path, f))
            dts[dt_name].add_data_unit(du)
    except OSError as e:
        if e.errno == 2:
            # That directory doesn't exist
            pass
        else: raise

for dt in dts:
    pl.run(dts[dt])
