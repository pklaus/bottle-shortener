
class ContainerPlugin(object):
    # http://docs.python.org/3.3/reference/datamodel.html#sequence-types
    def __len__(self):
        raise NotImplementedError()
    def __getitem__(self, key):
        raise NotImplementedError()
    def __setitem__(self, key, value):
        raise NotImplementedError()
    def __delitem__(self, key):
        raise NotImplementedError()
    def __iter__(self):
        raise NotImplementedError()
    def iterkeys(self):
        raise NotImplementedError()
    def __contains__(self, key):
        raise NotImplementedError()

class DictContainer(dict, ContainerPlugin):
    pass

import sqlite3
class SQLiteContainer(ContainerPlugin):
    db = None
    def __init__(self, dbfile=':memory:'):
        self.dbfile = dbfile
        try:
            self.db = sqlite3.connect(dbfile)
            self.db.row_factory = sqlite3.Row
            self.cur = self.db.cursor()
            self.cur.execute('SELECT SQLITE_VERSION()')
            data = self.cur.fetchone()
            print("SQLite version: %s" % data)
        except lite.Error as e:
            raise NameError("Error %s:" % e.args[0])
    def _commit(self):
        self.db.commit()
