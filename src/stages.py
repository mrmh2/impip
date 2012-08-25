#!/usr/bin/env python

import os

class DataStage:
    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return "DataStage, description: %s" % self.description

class DataUnit:
    def __init__(self, datastage):
        self.datastage = datastage

    def __repr__(self):
        return "DataStage, filename: %s" % self.filename

    def set_filename(self, filename):
        if not os.path.isfile(filename):
            # TODO: Better with an exception
            print "Error: %s does not exist or is not a file" % filename
        else:
            self.filename = filename

class ProcessStage:
    def __init__(self):
        self.command = None

class Connector:
    def __init__(self, dfrom, dto, process):
        pass
