##########################################################
# © 2011 Daniel 'grindhold' Brendle with torservers.net
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
###########################################################

import pgdb

ADDRESS = "127.0.0.1"
SCHEMA = "torcollect"
USER = "torcollect"
PASSWORD = "test"

# TODO: Store those values in configfile


class Database(object):
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = pgdb.connect(dsn="%s:%s" % (ADDRESS, SCHEMA),
                                           user=USER,
                                           password=PASSWORD)
        return self.connection

    def cursor(self):
        return self.get_connection().cursor()

    def commit(self):
        self.get_connection().commit()
