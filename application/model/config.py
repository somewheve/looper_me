from application.model.base import SqliteClient

from application.config import CONFIG_SQL, CONFIG_TABLENAME, CONFIG_DBNAME


class Config(SqliteClient):
    def load_config(self):
        res = self.query('config_name', 'config_value')
        print(res)
        data = {}
        for i in res:
            data[i[0]] = i[1]
        return data


config_db = Config(db_name=CONFIG_DBNAME, tablename=CONFIG_TABLENAME, sql=CONFIG_SQL)
