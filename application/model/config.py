from application.model.base import SqliteClient

from application.db_config import CONFIG_SQL, CONFIG_TABLENAME, CONFIG_DBNAME
from application.global_variable import KEY, AUTH_REQUIRED, ORIGIN_NUMBER


class Config(SqliteClient):
    def load_config(self):
        res = self.query('config_name', 'config_value')
        print(res)
        data = {}
        for i in res:
            data[i[0]] = i[1]
        return data


config_db = Config(db_name=CONFIG_DBNAME, tablename=CONFIG_TABLENAME, sql=CONFIG_SQL)
try:
    config_db.push(config_name='KEY', config_value=KEY)
    config_db.push(config_name='AUTH_REQUIRED', config_value=AUTH_REQUIRED)
    config_db.push(config_name='ORIGIN_NUMBER', config_value=ORIGIN_NUMBER)
except:
    pass
