#!/usr/bin/env python

import simpip
import pipeline
import os, sys
import pprint

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

def dataset_from_dir(dataset_name, data_dir):
    pl = simpip.create_pipeline()
    ds = pipeline.DataSet(dataset_name, pl)
    dts = data_tracks_from_path(data_dir, pl)
    for dtn in dts:
        ds.add_data_track(dts[dtn])

    return ds

def get_data_file(dataset_name):
    dir_name = 'data'
    data_dir = os.path.join(dir_name, dataset_name)
    ds = dataset_from_dir(dataset_name, data_dir)
    d = ds.get_data()
    
    return d

def main():
    try:
        dataset_name = sys.argv[1]
    except IndexError:
        print "Usage %s dataset_name" % os.path.basename(sys.argv[0])
        sys.exit(0)

    d = get_data_file(dataset_name)

    pprint.pprint(d)

if __name__ == '__main__':
    main()
