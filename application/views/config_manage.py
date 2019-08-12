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
        data = dict(key=tornado.options.options.KEY, auth_required=tornado.options.options.AUTH_REQUIRED,
                    origin_number=tornado.options.options.ORIGIN_NUMBER)
        self.write(true_return(data=data))

    def post(self):
        tornado.options.options.KEY = self.get_argument('key')
        auth_required = int(self.get_argument('auth_required'))
        tornado.options.options.AUTH_REQUIRED = bool(auth_required)
        tornado.options.options.ORIGIN_NUMBER = int(self.get_argument('origin_number'))
        config_db.update(key=tornado.options.options.KEY, auth_required=auth_required,
                         origin_number=tornado.options.options.ORIGIN_NUMBER)
        self.write(true_return(msg='更新成功'))
