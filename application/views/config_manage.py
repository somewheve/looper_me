"""
config views ----->
后台管理 config视图函数
"""
from application.model import config_db
from application.views import BaseHandle
from application.common.response_structure import true_return, false_return
import tornado.options


class ConfigHandler(BaseHandle):
    def get(self):
        data = config_db.load_config()
        self.write(true_return(data=data))

    def post(self):
        tornado.options.options.KEY = self.get_argument('KEY')
        AUTH_REQUIRED = int(self.get_argument('AUTH_REQUIRED'))
        tornado.options.options.AUTH_REQUIRED = bool(AUTH_REQUIRED)
        tornado.options.options.ORIGIN_NUMBER = int(self.get_argument('ORIGIN_NUMBER'))
        config_db.update(KEY=tornado.options.options.KEY)
        config_db.update(AUTH_REQUIRED=AUTH_REQUIRED)
        config_db.update(ORIGIN_NUMBER=tornado.options.options.ORIGIN_NUMBER)
        self.write(true_return(msg='更新成功'))
