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
            self.connection = pgdb.connect(dsn="%s:%s"%(ADDRESS,SCHEMA),
                                           user=USER,
                                           password=PASSWORD)
        return self.connection

    def cursor(self):
        return self.get_connection().cursor()

    def commit(self):
        self.get_connection().commit()

