"""
blacklist views ----->
后台管理 blacklist视图函数
"""
from application.model import blacklist_db
from application.views import BaseHandle
from application.tcp_server import md_server
from application.common import true_return, false_return, echo
from application.views.auth import auth_required


class BlacklistHandler(BaseHandle):
    @auth_required
    def get(self):
        data = []
        for ip in list(blacklist_db.load_ip()):
            data.append({'ip': ip})
        self.write(true_return(data=data))

    @auth_required
    def post(self):
        ip = self.get_argument('ip', None)
        todo = self.get_argument('todo', None)
        if not ip or not todo: return
        echo(todo, ip)

        if todo == 'alive':
            md_server.blacklist.remove(ip)

            blacklist_db.delete(ip)
            self.write(true_return(msg='解封成功'))
        else:
            self.write(false_return(msg='解封失败'))
