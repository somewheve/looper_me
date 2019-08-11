from application.model.base import SqliteClient

from application.db_config import CONFIG_SQL, CONFIG_TABLENAME, CONFIG_DBNAME
from application.global_variable import KEY, ORIGIN_NUMBER, AUTH_REQUIRED
import tornado.options


class Config(SqliteClient):
    def load_config(self):
        res = self.query('key', 'origin_number', 'auth_required')
        data = {}
        for i in res:
            data['KEY'] = i[0]
            data['ORIGIN_NUMBER'] = i[1]
            data['AUTH_REQUIRED'] = i[2]
        return data


config_db = Config(db_name=CONFIG_DBNAME, tablename=CONFIG_TABLENAME, sql=CONFIG_SQL)
try:
    config_db.push(KEY=KEY, AUTH_REQUIRED=AUTH_REQUIRED, ORIGIN_NUMBER=ORIGIN_NUMBER)
except:
    tornado.options.options.KEY = config_db.load_config().get('KEY')
    tornado.options.options.ORIGIN_NUMBER = config_db.load_config().get('ORIGIN_NUMBER')
    tornado.options.options.AUTH_REQUIRED = bool(config_db.load_config().get('AUTH_REQUIRED'))
