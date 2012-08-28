#!/usr/bin/env python

import simpip
import pipeline
import os

def get_prefix(f):
    p, e = os.path.splitext(f)
    return p

def data_tracks_from_path(data_dir, pl):
    dts = {}
    for ds_name in pl.dstages:
        ds_path = os.path.join(data_dir, pipeline.squash_name(ds_name))
        try:
            for f in os.listdir(ds_path):
                #print ds_name, ds_path, f
                dt_name = get_prefix(f)
                if dt_name not in dts:
                    #print "Creating %s" % dt_name
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

    return dts

def main():
    pl = simpip.create_pipeline()
    data_dir = 'data/newexp'
    dts = data_tracks_from_path(data_dir, pl)
    for dt in dts:
        pl.run(dts[dt])

if __name__ == '__main__':
    main()
