from rethinkdb import RethinkDB
from rethinkdb.errors import RqlRuntimeError
import uuid

class DB():
    def __init__(self, dbConf ):
        self.dbConf = dbConf
        self.db_init()
    
    def db_init(self):
        self.db_host = self.dbConf['db_host']
        self.db_user = self.dbConf['db_user']
        self.db_pass = self.dbConf['db_pass']
        self.db_port = self.dbConf['db_port']

        self.r = RethinkDB()
        self.conn  = self._conn()

    def db_create(self):
        # check if db exists
        exists = self.r.db_list().contains(self.dbConf['db_name']).run(self.conn)
        if not exists:
            resp = self.r.db_create( self.dbConf['db_name'] ).run(self.conn)
            exists = resp['dbs_created']

        table_created = {}
        if exists:
            # create tables
            if len(self.dbConf['table_list']) > 0:
                for table in self.dbConf['table_list']:
                    tb_exists = self.r.db(self.dbConf['db_name']).table_list().contains(table).run(self.conn)
                    if not tb_exists:
                        primary_key = self.dbConf['db_name'] + '_id'
                        table_created[table] = self.r.db(self.dbConf['db_name']).table_create(table).run(self.conn)

    def _conn(self):
        try:
            conn = self.r.connect(host=self.db_host, port=self.db_port, user=self.db_user, password=self.db_pass)
        except RqlRuntimeError as err:
            print('Error', err.message)
            conn = False
        return conn

    def close(self):
        if self.conn:
            self.conn.close()

    def uuid(self):
        return str(uuid.uuid4())
