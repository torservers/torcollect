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
    def __init__(self):
        self.id = None
        self.name = ""

    def store(self):
	""" Stores this bridge in the database or creates it newly """
        pass

    def delete(self):
	""" removes this bridge from the database"""
        pass

    def get_bridges(self):
	""" returns bridges that have only been disclosed to this organization"""
	pass
