"""
config views ----->
后台管理 config视图函数
"""
from application.model import config_db
from application.views import BaseHandle
from application.common.response_structure import true_return, false_return


class ConfigHandler(BaseHandle):
    def get(self):
        data = config_db.load_config()
        self.write(true_return(data=data))

    def post(self):
        config_name = self.get_argument('config_name')
        config_value = self.get_argument('config_value', None)
        todo = self.get_argument('todo')
        if todo == 'update':
            config_db.update(config_value=config_value, condition=f'config_name="{config_name}"')
            self.write(true_return(msg='更新成功'))
        elif todo == 'delete':
            config_db.pop(config_name=config_name)
            self.write(true_return(msg='删除成功'))
        elif todo == 'insert':
            config_db.push(config_name=config_name, config_value=config_value)
            self.write(true_return(msg='添加成功'))
        else:
            self.write(false_return(msg="参数错误"))
