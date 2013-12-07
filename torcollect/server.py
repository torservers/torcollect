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
        self.keyfile  = ""
    
    def get_name(self):
        return self.name

    def get_ip(self):
        return self.ip

    @classmethod
    def load(cls, address):
        pass

    @classmethod
    def create(cls, address, name, port, password, keyfile):
        server = Server()
        server.ip = address
        server.name = name
        server.port = port
        server.password = password
        if keyfile is not None:
            server.login_type = LoginType.PUBLICKEY
            server.keyfile = keyfile
        else:
            server.login_type = LoginType.PASSWORD
        return server        

    @classmethod
    def get_server_list(cls):
        db = torcollect.database.Database()
        cur = db.cursor()
        stmnt = "SELECT SRV_NAME, SRV_IP FROM Server;"
        ret = []
        for name, ip in cur.fetchall():
            srv = Server()
            srv.ip = ip
            srv.name = name
        return ret

    def store(self):
        db = torcollect.database.Database()
        cur = db.cursor()
        if self.id is None:
            stmnt = "INSERT INTO Server (SRV_IP, SRV_NAME) VALUES (%(ip)s,%(name)s) RETURNING SRV_ID;"
            cur.execute(stmnt, {'ip':self.ip, 'name':self.name})
            self.id = cur.fetchone()[0]
        else:
            stmnt = "UPDATE SERVER SET SRV_NAME = %(name)s, SRV_IP = %(ip)s  WHERE SRV_ID = %(id)d;"
            cur.execute(stmnt, {'ip':self.ip, 'name':self.name, 'id':self.id})

    def delete(self):
        db = torcollect.database.Database()
        cur = db.cursor()
        stmnt = "DELETE FROM SERVERS WHERE SRV_ID = %(id)d;"
        cur.execute(stmnt, {'id':self.id})

