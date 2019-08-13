"""
blacklist views ----->
后台管理 blacklist视图函数
"""
from application.model import admin_db, session
from application.views import BaseHandle
from application.common import true_return, false_return
from application.views.auth import auth_required, Auth


class AdminLoginHandler(BaseHandle):
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if username and password:
            self.write(Auth.authenticate(username, password))
        else:
            self.write(false_return(msg='用户名或密码错误'))


class AdminChangepwdHandler(BaseHandle):
    @auth_required
    def post(self):

        old_pwd = self.get_argument('old_pwd')
        new_pwd1 = self.get_argument('new_pwd1')
        new_pwd2 = self.get_argument('new_pwd2')
        if not old_pwd or not new_pwd1 or not new_pwd2:
            self.write(false_return(msg='含空项'))
            return

        if new_pwd1 != new_pwd2:
            self.write(false_return(msg='密码不一致'))
            return

        admin = session.query(admin_db).filter_by(uid=self.current_user.uid).first()

        if admin.update_password(old_pwd, new_pwd1):
            self.write(true_return(msg='修改密码成功！'))
        else:
            self.write(false_return(msg='密码错误'))
