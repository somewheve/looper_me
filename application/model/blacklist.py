from application.model.base import SqliteClient

from application.config import BLACKLIST_TABLENAME, BLACKLIST_SQL, BLACKLIST_DBNAME


class Blacklist(SqliteClient):
    def load_ip(self):
        res = self.query('ip')
        data = set()
        for i in res:
            data.add(i[0])
        return data


blacklist_db = Blacklist(db_name=BLACKLIST_DBNAME, tablename=BLACKLIST_TABLENAME, sql=BLACKLIST_SQL)
