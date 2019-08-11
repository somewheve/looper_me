from application.model.base import SqliteClient

from application.db_config import CONFIG_SQL, CONFIG_TABLENAME, CONFIG_DBNAME
from application.global_variable import variable
import tornado.options

class Config(SqliteClient):
    def load_config(self):
        res = self.query('config_name', 'config_value')
        data = {}
        for i in res:
            if i[0] == 'AUTH_REQUIRED':
                data[i[0]] = bool(int(i[1]))
            data[i[0]] = i[1]
        return data


config_db = Config(db_name=CONFIG_DBNAME, tablename=CONFIG_TABLENAME, sql=CONFIG_SQL)
try:
    for k, v in variable.items():
        config_db.push(config_name=k, config_value=v)
except:
    tornado.options.options.variable = config_db.load_config()
