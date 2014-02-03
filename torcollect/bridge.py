#-*- coding: utf-8 -*-

###########################################################
# © 2013/2014 Daniel 'grindhold' Brendle with torservers.net
#
# This file is part of torcollect
#
# torcollect is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later
# version.
#
# torcollect is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with torcollect.
# If not, see http://www.gnu.org/licenses/.
############################################################

import torcollect.paths
import torcollect.database

class Bridge(object):
    def __init__(self):
        self.ip = ""
        self.server = ""
    
    @classmethod
    def list(cls, server=""):
        db = torcollect.database.Database()
        server = "%"+server+"%"
        stmnt = "SELECT BRG_ID, SRV_NAME, BRG_NR \
                 FROM Bridge INNER JOIN Server \
                    ON (BRG_SRV_ID = SRV_ID) \
                 WHERE SRV_NAME LIKE %(server)s;"
        cur = db.cursor()
        cur.execute(stmnt, {'server':server})
        ret = []
        for dataset in cur.fetchall():
            ret.append({'id': dataset[0],
                        'srv_name': dataset[1],
                        'nr': dataset[2]})
        return ret
                         

    def setup_db(self):
        """ Create a new database for this bridge"""
    	pass

    def disclose_to(self, organization):
	""" Disclose this bridge only to a specific organization """
        pass
 
