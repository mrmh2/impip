#import simpip
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

def dataset_from_dir(dataset_name, data_dir, pipeline_name):
    pline = __import__(pipeline_name)
    pl = pline.create_pipeline()
    ds = pipeline.DataSet(dataset_name, pl)
    dts = data_tracks_from_path(data_dir, pl)
    for dtn in dts:
        ds.add_data_track(dts[dtn])

    return ds

#def get_data_files(dataset_name, pipeline_name='simpip'):
#    dir_name = 'data'
#    data_dir = os.path.join(dir_name, dataset_name)
#    ds = dataset_from_dir(dataset_name, data_dir, pipeline_name)
#    d = ds.get_data()
#    
#    return d
