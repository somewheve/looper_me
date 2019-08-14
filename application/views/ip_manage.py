"""
ip_manage views ----->
后台管理 ip视图函数
"""
from application.views import BaseHandle
from application.tcp_server import md_server
from application.common import true_return, false_return, echo
from application.model import blacklist_db
from application.views.auth import auth_required


class IpHandler(BaseHandle):
    @auth_required
    def get(self):
        data = []
        for ip in list(md_server.global_connection.keys()):
            data.append({'ip': ip})
        self.write(true_return(data=data))

    @auth_required
    def post(self):
        ip = self.get_argument('ip', None)
        todo = self.get_argument('todo', None)
        if not ip or not todo: return
        echo(todo, ip)

        if ip in md_server.global_connection:
            md_server.global_connection.pop(ip).close()  # 断开连接
        if ip in md_server.tick_origin:
            md_server.tick_origin.remove(ip)  # 源服务器弹出

        if todo == 'kill':
            self.write(true_return(msg='封禁成功'))
        if todo == 'pull_black':
            md_server.blacklist.add(ip)  # 拉黑
            blacklist_db.add(ip)  # 存入数据库
            self.write(true_return(msg='拉黑成功'))
        else:
            self.write(false_return(msg='操作失败'))
