#-*- coding: utf-8 -*-

##########################################################
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
###########################################################

import torcollect.database


class LoginType:
    PASSWORD = 0
    PUBLICKEY = 1


class Server(object):
    def __init__(self):
        #server-information
        self.id = None
        self.ip = ""
        self.name = ""
        #auth-information
        self.login_type = None
        self.port = 22
        self.username = ""
        self.password = ""
        self.keyfile = ""

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_login_type(self):
        return self.login_type

    def get_keyfile(self):
        return self.keyfile

    @classmethod
    def load(cls, address_or_id):
        """ load a server by address or id. assume id, when the input is
            an integer, assume it's an address when input is a string
        """
        db = torcollect.database.Database()
        cur = db.cursor()
        if type(address_or_id) == str:
            stmnt = "SELECT SRV_ID, SRV_NAME, LGI_AUTHTYPE, LGI_SSHPORT, \
                     LGI_USER, LGI_PASSWORD, LGI_KEYFILE, SRV_IP \
                     FROM Server INNER JOIN Login \
                       ON (LGI_SRV_ID = SRV_ID) \
                     WHERE SRV_IP = %(address)s;"
        elif type(adress_or_id) == int:
            stmnt = "SELECT SRV_ID, SRV_NAME, LGI_AUTHTYPE, LGI_SSHPORT, \
                     LGI_USER, LGI_PASSWORD, LGI_KEYFILE, SRV_IP \
                     FROM Server INNER JOIN Login \
                       ON (LGI_SRV_ID = SRV_ID) \
                     WHERE SRV_ID = %(id)d;"
        else:
            return # Invalid input
        cur.execute(stmnt, {"address": address})
        res = cur.fetchone()
        server = Server()
        server.id = res[0]
        server.ip = res[7]
        server.name = res[1]
        server.login_type = res[2]
        server.port = res[3]
        server.username = res[4]
        server.password = res[5]
        server.keyfile = res[6]
        return server

    @classmethod
    def create(cls, address, name, port, user, password, keyfile):
        server = Server()
        server.ip = address
        server.name = name
        server.port = port
        server.username = user
        server.password = password
        if keyfile is not None:
            server.login_type = LoginType.PUBLICKEY
            server.keyfile = keyfile
        else:
            server.login_type = LoginType.PASSWORD
        return server

    @classmethod
    def get_server_list(cls, full=False):
        db = torcollect.database.Database()
        cur = db.cursor()
        if not full:
            stmnt = "SELECT SRV_NAME, SRV_IP FROM Server;"
        else:
            stmnt = "SELECT SRV_NAME, SRV_IP, SRV_ID,  LGI_AUTHTYPE,\
                     LGI_SSHPORT, LGI_USER, LGI_PASSWORD, LGI_KEYFILE \
                     FROM Login INNER JOIN Server \
                       ON (LGI_SRV_ID = SRV_ID);"
        cur.execute(stmnt)
        ret = []
        for row in cur.fetchall():
            srv = Server()
            print row
            srv.name = row[0]
            srv.ip = row[1]
            if full:
                srv.id = row[2]
                srv.login_type = row[3]
                srv.port = row[4]
                srv.username = row[5]
                srv.password = row[6]
                srv.keyfile = row[7]
            ret.append(srv)
        return ret

    def store(self):
        db = torcollect.database.Database()
        cur = db.cursor()
        if self.id is None:
            stmnt = "INSERT INTO Server (SRV_IP, SRV_NAME)\
                    VALUES (%(ip)s,%(name)s) RETURNING SRV_ID;"
            cur.execute(stmnt, {'ip': self.ip, 'name': self.name})
            self.id = cur.fetchone()[0]

            if self.login_type == LoginType.PASSWORD:
                stmnt = "INSERT INTO Login (LGI_AUTHTYPE, LGI_SSHPORT,\
                         LGI_USER, LGI_PASSWORD, LGI_SRV_ID) \
                         VALUES (%(auth)d, %(ssh)d,\
                         %(user)s, %(pw)s, %(srv_id)d);"
                cur.execute(stmnt, {'auth': self.login_type,
                                    'ssh': int(self.port),
                                    'user': self.username,
                                    'pw': self.password,
                                    'srv_id': self.id})
            elif self.login_type == LoginType.PUBLICKEY:
                # TODO: PublicKey File can only be a textfile by now
                #       Don't know whether binary keyfiles will be needed
                #       In the future
                stmnt = "INSERT INTO Login (LGI_AUTHTYPE, LGI_SSHPORT,\
                         LGI_USER, LGI_PASSWORD, LGI_KEYFILE, LGI_SRV_ID) \
                        VALUES  (%(auth)d, %(ssh)d, %(user)s, %(pw)s, \
                        %(keyfile)s, %(srv_id)d);"
                cur.execute(stmnt, {'auth': self.login_type,
                                    'ssh': int(self.port),
                                    'user': self.username,
                                    'pw': self.password,
                                    'keyfile': self.keyfile,
                                    'srv_id' : self.id})
        else:
            stmnt = "UPDATE SERVER SET SRV_NAME = %(name)s, SRV_IP = %(ip)s\
                     WHERE SRV_ID = %(id)d;"
            cur.execute(stmnt,
                        {'ip': self.ip, 'name': self.name, 'id': self.id})
        db.commit()

    def delete(self):
        db = torcollect.database.Database()
        cur = db.cursor()
        stmnt = "DELETE FROM Server WHERE SRV_ID = %(id)d;"
        cur.execute(stmnt, {'id': self.id})
        db.commit()
