"""
origin_manage views ----->
后台管理 origin视图函数
"""
from application.model import blacklist_db
from application.views import BaseHandle
from application.tcp_server import md_server
from application.common import true_return, false_return, echo
from application.views.auth import auth_required


class OriginHandler(BaseHandle):
    @auth_required
    def get(self):
        data = []
        for ip in md_server.tick_origin:
            data.append({'ip': ip})
        self.write(true_return(data=data))

    @auth_required
    def post(self):
        ip = self.get_argument('ip', None)
        todo = self.get_argument('todo', None)
        if not ip or not todo: return
        echo(todo, ip)

        md_server.global_connection.pop(ip).close()  # 断开连接
        md_server.tick_origin.remove(ip)  # 源服务器弹出

        if todo == 'kill':
            self.write(true_return(msg='封禁成功'))

        elif todo == 'pull_black':
            md_server.blacklist.add(ip)  # 拉黑
            blacklist_db.add(ip)  # 写入数据库
            self.write(true_return(msg='拉黑成功'))
        else:
            self.write(false_return(msg='操作失败'))
