#!/usr/bin/env python

import os
import errno
import shutil
import sys
import logging
import pprint

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logging.NOTE = 32
logging.addLevelName(logging.NOTE, 'NOTE')
logger.note = lambda msg, *args: log._log(logging.NOTE, msg, args)

filehdlr = logging.FileHandler('log/pipeline.log')
filehdlr.setLevel(logging.DEBUG)
logger.addHandler(filehdlr)

strmhdlr = logging.StreamHandler(sys.stdout)
strmhdlr.setLevel(logging.INFO)
logger.addHandler(strmhdlr)

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
        self.dunits = {}
        self.init_logger()

        self.connections = []

    def __repr__(self):
        return "Pipeline, name: %s" % self.name

    def create_data_stage(self, dstagename):
        ds = DataStage(dstagename)
        self.add_data_stage(ds)

    def create_process_stage(self, pstagename, modname, ext='.png'):
        ps = ProcessStage(pstagename, modname, ext)
        self.add_processing_stage(ps)

    def init_logger(self):
        self.logger = logging.getLogger(__name__)

    def add_data_stage(self, dstage):
        self.dstages[dstage.name] = dstage

    def add_processing_stage(self, pstage):
        self.pstages[pstage.name] = pstage
        #od = os.path.join(self.data_dir, squash_name(pstage.name))
        #pstage.set_output_dir(od)

    def add_data_unit(self, dunit):
        self.dunits[dunit.filename] = dunit

    def connect(self, dstage1, pstage, dstage2):
        pstage.add_input(dstage1)
        pstage.add_output(dstage2)
        #dstage1.connect(pstage, dstage2)

    def connect_by_name(self, ndstage1, npstage, ndstage2):
        try:
            pstage = self.pstages[npstage]
        except KeyError, e:
            print "ERROR: Process stage %s does not exist" % e
            sys.exit(2)
        try:
            dstage1 = self.dstages[ndstage1]
            dstage2 = self.dstages[ndstage2]
        except KeyError, e:
            print "ERROR: Data stage %s does not exist" % e
            sys.exit(2)

        self.connect(dstage1, pstage, dstage2)
        self.connections.append((ndstage1, npstage, ndstage2))

    def run(self, dataset):
        for dtn, datatrack in dataset.dtracks.iteritems():
            for pname, pstage in self.pstages.iteritems():
                pstage.run(datatrack)

    def run_single_track(self, datatrack):
        for pname, pstage in self.pstages.iteritems():
            pstage.run(datatrack)

class DataStage:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "DataStage, name: %s" % self.name

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

class ProcessStage(object):
    def __init__(self, name, filtname, ext='.png'):
        self.name = name
        self.ext = ext
        self.filtname = filtname
        self.logger = logging.getLogger(__name__)

        self.inputs = {}
        self.outputs = {}

    def add_input(self, dstage):
        self.inputs[dstage.name] = dstage

    def add_output(self, dstage):
        self.outputs[dstage.name] = dstage

    def set_output(self, dstage):
        self.output_dstage = dstage

    def set_output_dir(self, outdir):
        self.output_dir = outdir

    def execute(self, input_filename, output_filename):
        self.logger.info("Executing %s on %s to produce %s" % 
            (self.filtname, input_filename, output_filename))
        pfilt = __import__(self.filtname)
        pfilt.process(input_filename, output_filename)

    def run(self, data_track):
        self.logger.info("Running stage %s on data track %s" % (self.name, data_track.name))
        # TODO - process modules need to know which input is which somehow
        infiles = []
        for name, dstage in self.inputs.iteritems():
            # TODO - modification time stuff will go in here
            fn = data_track.get_filename(dstage)
            infiles.append(fn)

        if not all(infiles):
            logger.info("Not enough input files for applying %s to %s", self.name, data_track.name)
            return

        existing_outfiles = []
        for name, dstage in self.outputs.iteritems():
            fn = data_track.get_filename(dstage)
            existing_outfiles.append(fn)

        if any(existing_outfiles):
            logger.info("At least one output file exists, not overwriting %s on %s", 
                self.name, data_track.name)
            return

        outfiles = []
        for name, dstage in self.outputs.iteritems():
            fn = data_track.get_suggested_filename(dstage, self.ext)
            mkdir_p(os.path.dirname(fn))
            outfiles.append((name, fn))

        od = dict(outfiles)

        try:
            outfiles = [od[o] for o in self.output_map]
        except AttributeError:
            outfiles = od.values()

        if len(infiles) and len(outfiles):
            if len(outfiles) == 1 and len(infiles) == 1: 
                self.execute(infiles[0], outfiles[0])
            else:
                self.execute(infiles, outfiles)
        else:
            logger.info("Processing stage %s has either no inputs or no outputs" % self.name)

    def orun(self, input_filename, output_prefix):
        # TODO - split this up
        self.logger.info("Running processing stage %s on %s" % (self.name, input_filename))
        in_file, in_ext = os.path.splitext(os.path.basename(input_filename))
        output_filename = in_file + self.ext
        output_path = os.path.join(output_prefix, squash_name(self.output_dstage.name))
        # TODO - probably do this elsewhere
        mkdir_p(output_path)
        output_fullname = os.path.join(output_path, output_filename)
        self.logger.debug("  I will create %s" % output_fullname)

        if os.path.isfile(output_fullname) or os.path.exists(output_fullname):
            self.logger.debug("    Output file/dir already exists")
        else:
            self.logger.debug("    File/dir does not exist")
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

    def get_filename(self, data_stage):
        logger.debug("DataTrack) Retrieving filename for %s of %s" % (data_stage.name, self.name))
        for dun, dunit in self.dunits.iteritems():
            if data_stage.name == dunit.dstage.name:
                return dun

        return None

    def get_suggested_filename(self, data_stage, ext):
        dd = self.data_dir
        fd = squash_name(data_stage.name)
        fn = self.name + ext

        return os.path.join(dd, fd, fn)

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
