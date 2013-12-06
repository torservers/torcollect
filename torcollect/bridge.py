import rrdtool
import torcollect.paths

class Bridge(object):
    def __init__(self):
        self.ip = ""
        self.server = ""
    
    def setup_db(self):
        """ Create a new database for this bridge"""
        rrdtool.create('/tmp/test.rrd', 'DS:foo:GAUGE:20:0:U')
        
