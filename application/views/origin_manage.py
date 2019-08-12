"""
origin_manage views ----->
后台管理 origin视图函数
"""
from application.model import blacklist_db
from application.views import BaseHandle
from application.tcp_server import md_server
from application.common import true_return, false_return


class OriginHandler(BaseHandle):
    def get(self):
        data = []
        for ip in list(md_server.tick_origin):
            data.append({'ip': ip})
        self.write(true_return(data=data))

    def post(self):
        ip = self.get_argument('ip', None)
        todo = self.get_argument('todo', None)
        if not ip or not todo: return
        print(todo, ip)

        if todo == 'kill':
            md_server.global_connection.pop(ip).close()
            self.write(true_return(msg='封禁成功'))
        elif todo == 'pull_black':
            md_server.global_connection.pop(ip).close()
            md_server.blacklist.add(ip)
            blacklist_db.add(ip)
            self.write(true_return(msg='拉黑成功'))
        else:
            self.write(false_return(msg='操作失败'))
