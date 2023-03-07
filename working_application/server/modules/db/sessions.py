from modules.db.db import DB

class SessionHandler(DB):
    tb_sessions = "sessions"
    tb_session_index = "sessions_id"
    def __init__(self, dbConf):
        super().__init__(dbConf)

    def session_exists(self, sess_id):
        entry = self.r.db( self.dbConf['db_name'] ).table(self.tb_sessions).get(sess_id).run(self.conn)
        return entry

    def session_register(self, session):
        inserted = self.r.db(self.dbConf['db_name']).table(self.tb_sessions).insert(session).run(self.conn)
        return inserted

    def session_update(self, sess_id, session ):
        updated = self.r.db(self.dbConf['db_name']).table(self.tb_sessions).get(sess_id).update(session).run(self.conn)
        return updated

    def get_all(self):
        result = self.r.db(self.dbConf['db_name']).table(self.tb_sessions).run(self.conn)
        return result