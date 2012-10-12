import os
import itertools

import pipeline

def generate_name(basepath, path):
    basename = os.path.basename(basepath)
    return path[path.find(basename):]

def multiple_datasets_from_path(path, pl):

    walk = [(r, ds) for r, ds, fs in os.walk(path) if len(ds)]
    full_dirs_paths = [[os.path.join(r, d) for d in ds] for r, ds in walk]
    dirlist = list(itertools.chain(*full_dirs_paths))

    datasets = [dataset_from_dir(generate_name(path, f), f, pl) 
        for f in dirlist]

    return [ds for ds in datasets if ds.size]

def load_pipeline_by_name(plname):
    pline = __import__(plname)
    return pline.create_pipeline()

def get_prefix(f):
    p, e = os.path.splitext(f)
    return p

def data_tracks_from_path(data_dir, pl):
    dts = {}
    for ds_name in pl.dstages:
        ds_path = os.path.join(data_dir, pipeline.squash_name(ds_name))
        try:
            #print 'Trying', ds_path
            for f in os.listdir(ds_path):
                #print ds_name, ds_path, f
                dt_name = get_prefix(f)
                #print "dt_name is %s" % dt_name
                if dt_name not in dts:
                    #print "Creating %s" % dt_name
                    dts[dt_name] = pipeline.DataTrack(dt_name, pl, data_dir)
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

def dataset_from_dir(dataset_name, data_dir, pl):

    ds = pipeline.DataSet(dataset_name, pl)
    dts = data_tracks_from_path(data_dir, pl)
    for dtn in dts:
        ds.add_data_track(dts[dtn])

    return ds
