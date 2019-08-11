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
        tornado.options.optionsvariable = self.get_body_argument()
        for k, v in self.get_body_argument():
            config_db.update(config_value=self.get_argument(k), condition=f'config_name="{v}"')
        self.write(true_return(msg='更新成功'))
