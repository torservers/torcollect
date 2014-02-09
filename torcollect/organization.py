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

from torcollect.database import Database

class Organization(object):
    @classmethod
    def load(cls, nr):
        """ Loads the organization with the given ID """
        db = Database()
        stmnt = "SELECT ORG_NAME FROM Organization WHERE ORG_ID = %(id)d;"
        cur = db.cursor()
        cur.execute(stmnt, {'id': nr})
        res = cur.fetchone()
        if res is None:
            return
        o = Organization()
        o.name = res[0]
        o.id = nr
        return o
    
    @classmethod
    def list(cls):
        db = Database()
        stmnt = "SELECT ORG_ID, ORG_NAME FROM Organization;"
        cur = db.cursor()
        cur.execute(stmnt)
        res = cur.fetchall()
        ret = []
        for set in res:
            ret.append({'id':set[0],
                        'name':set[1]})
        return ret

    def __init__(self):
        self.id = None
        self.name = ""
    
    def get_id(self):
        return self.id
    
    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def store(self):
    	""" Stores this bridge in the database or creates it newly """
        db = Database()
        cur = db.cursor()
        if self.id is None:
            # Create new Organization in database
            stmnt = "INSERT INTO Organization (ORG_NAME) \
                        VALUES (%(name)s) RETURNING ORG_ID;"
            cur.execute(stmnt, {'name': self.name})
            self.id = cur.fetchone()[0] # set automatically given id to self
        else:
            # Update existing Organization
            stmnt = "UPDATE Organization SET ORG_NAME = %(name)s \
                        WHERE ORG_ID = %(id)d;"
            cur.execute(stmnt, {'id': self.id,
                                'name': self.name})
        db.commit()
        

    def delete(self):
    	""" removes this bridge from the database"""
        db = Database()
        stmnt = "DELETE FROM Organization WHERE ORG_ID = %(id)d;"
        cur = db.cursor()
        cur.execute(stmnt, {'id': self.id})
        db.commit()

    def get_bridges(self):
    	""" returns bridges that have only been disclosed to this organization"""
        pass

    def disclose_bridge(self, bridge):
        """ Discloses a bridge to this organization """
        if type(bridge) != int:
            bridge = bridge.get_id()
        db = Database()
        stmnt = "INSERT INTO DisclosureTo (DSC_BRG_ID, DSC_ORG_ID) \
                    VALUES (%(brg_id)d, %(org_id)s);"
        cur = db.cursor()
        cur.execute(stmnt , {'brg_id' : bridge,
                             'org_id' : self.id})
        db.commit()
