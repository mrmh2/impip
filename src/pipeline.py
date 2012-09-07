#!/usr/bin/env python

import os, errno, shutil
import sys

def mprint(string):
    print string

def mkdir_p(path):
    try:
        os.makedirs(path)   
    except OSError as exc:
        # FIXME
        if exc.errno == 17:
        #if exc.errno == errno.EXIST:
            pass
        else: raise

def squash_name(name):
    return name.lower().replace(" ", "_")

class Pipeline:
    def __init__(self, name):
        self.dstages = {}
        self.pstages = {}
        self.name = name
        self.logger

        self.dunits = {}

    def __repr__(self):
        return "Pipeline, name: %s" % self.name

    def add_data_stage(self, dstage):
        self.dstages[dstage.name] = dstage

    def add_processing_stage(self, pstage):
        self.pstages[pstage.name] = pstage
        #od = os.path.join(self.data_dir, squash_name(pstage.name))
        #pstage.set_output_dir(od)

    def add_data_unit(self, dunit):
        self.dunits[dunit.filename] = dunit

    def connect(self, dstage1, pstage, dstage2):
        dstage1.connect(pstage, dstage2)

    def run(self, dataset):
        print "pipeline.run()"
        for dtn in dataset.dtracks:
            datatrack = dataset.dtracks[dtn]
            for du_filename in datatrack.dunits:
                du = datatrack.dunits[du_filename]
                mprint("  Processing unit %s" % du.filename)
                ds = du.dstage
                mprint("    at stage %s" % ds.name)
                ps = ds.output_pstage
                if ps:
                    mprint("    has pstage, %s" % ps.name)
                    ps.run(du.filename, datatrack.data_dir)

class DataStage:
    def __init__(self, name):
        self.name = name
        self.output_pstage = None

    def __repr__(self):
        return "DataStage, description: %s" % self.description

    def connect(self, pstage, dstage):
        # TODO - lists go here to allow multiplestuffs. Or connectors?
        self.output_pstage = pstage
        pstage.set_output(dstage)

class DataUnit:
    def __init__(self, datastage):
        self.dstage = datastage

    def __repr__(self):
        return "DataUnit, filename: %s" % self.filename

    def set_filename(self, filename):
        if not os.path.isfile(filename) and not os.path.exists(filename):
            # TODO: Better with an exception
            print "Error in setting DataUnit filename: %s does not exist or is not a file" % filename
            sys.exit(0)
        else:
            self.filename = filename

class ProcessStage:
    def __init__(self, name, filtname):
        self.command = None
        self.fnmapping = None
        self.name = name
        self.ext = '.png'
        self.filtname = filtname

    def set_output(self, dstage):
        self.output_dstage = dstage

    def set_output_dir(self, outdir):
        self.output_dir = outdir

    def execute(self, input_filename, output_filename):
        pfilt = __import__(self.filtname)
        pfilt.process(input_filename, output_filename)

    def run(self, input_filename, output_prefix):
        # TODO - split this up
        mprint("Running processing stage %s on %s" % (self.name, input_filename))
        in_file, in_ext = os.path.splitext(os.path.basename(input_filename))
        output_filename = in_file + self.ext
        output_path = os.path.join(output_prefix, squash_name(self.output_dstage.name))
        # TODO - probably do this elsewhere
        mkdir_p(output_path)
        output_fullname = os.path.join(output_path, output_filename)
        mprint("  I will create %s" % output_fullname)

        if os.path.isfile(output_fullname) or os.path.exists(output_fullname):
            mprint("    Output file/dir already exists")
        else:
            mprint("    File/dir does not exist")
            self.execute(input_filename, output_fullname)

class Connector:
    def __init__(self, dfrom, dto, process):
        pass

class DataTrack:
    def __init__(self, name, pipeline, data_dir):
        self.name = name
        self.prefix = name
        self.pipeline = pipeline
        self.dunits = {}

        self.set_data_dir(data_dir)

    def set_data_dir(self, dirname):
        self.data_dir = dirname

    def import_file(self, filename, dstage_name):
        print "Importing %s" % filename
        dstage = self.pipeline.dstages[dstage_name]
        du = DataUnit(dstage)
        du.set_filename(filename)

        output_path = os.path.join(self.data_dir, squash_name(dstage.name))
        output_filename = os.path.join(output_path, self.prefix + '.png')
        
        print "Will write as %s" % output_filename

        mkdir_p(output_path)
        shutil.copy(filename, output_filename)

        du.set_filename(output_filename)

        self.add_data_unit(du)

    def add_data_unit(self, dunit):
        self.dunits[dunit.filename] = dunit

    def get_data(self):
        d = {}

        for dun in self.dunits:
            d[self.dunits[dun].dstage.name] = dun

        return d

    def update():
        pass

class DataSet:
    def __init__(self, name, pipeline):
        self.name = name
        self.pipeline = pipeline
        self.dtracks = {}

    def add_data_track(self, dtrack):
        self.dtracks[dtrack.name] = dtrack

    def display(self):
        print "<=%s=>" % self.name
        for dsn in self.pipeline.dstages:
            print dsn,
        print ""

        for dtn in self.dtracks:
            print "DTN: %s" % dtn
            for dun in self.dtracks[dtn].dunits:
                print "  DTU: %s" % dun

    def get_data(self):
        d = {}

        for dtn in self.dtracks:
            d[dtn] = self.dtracks[dtn].get_data()

        return d
