import datetime
import json
from functools import wraps
import time
import jwt
from application.global_variable import JWT_SECRET_KEY
from application.model import admin_db, session
from application.common import true_return, false_return,echo


class Auth:
    @staticmethod
    def encode_auth_token(user_info):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        """
        "exp": 过期时间
        "nbf": 表示当前时间在nbf里的时间之前，则Token不被接受
        "iss": token签发者
        "aud": 接收者
        "iat": 发行时间
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2, seconds=0),
                # 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10),  #test
                'iat': datetime.datetime.utcnow(),
                'iss': 'looper_me',
                'data': user_info
            }
            return jwt.encode(
                payload,
                JWT_SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            echo(e,flag='ERROR')
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: dict|string
        """
        try:
            payload = jwt.decode(auth_token, JWT_SECRET_KEY, leeway=datetime.timedelta(seconds=10))
            # payload = jwt.decode(auth_token, JWT_SECRET_KEY, options={'verify_exp': False})# 取消过期时间验证
            if 'data' in payload and 'uid' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    @staticmethod
    def authenticate(username, password):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param username
        :param password
        :return: true_return(data=token.decode(), msg='登录成功')
        """
        user = session.query(admin_db).filter_by(username=username).first()
        if user is None:
            return false_return(msg='找不到用户')
        else:
            if user.check_password(password):
                login_time = int(time.time())
                user.login_time = login_time
                session.commit()

                user_info = {
                    "login_time": login_time,
                    "uid": user.uid
                }
                token = Auth.encode_auth_token(user_info)
                return true_return(data=token.decode(), msg='登录成功')
            else:
                return false_return(msg='密码不正确')

    @staticmethod
    def identify(request):
        """
        用户鉴权
        :return: list
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_tokenArr = auth_header.split(" ")
            if not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2:
                result = false_return(msg='请传递正确的验证头信息')
            else:
                auth_token = auth_tokenArr[1]
                payload = Auth.decode_auth_token(auth_token)
                if isinstance(payload, str):
                    result = false_return(msg=payload)
                else:
                    user = session.query(admin_db).filter_by(uid=payload['data']['uid']).first()
                    if user is None:
                        result = false_return(msg='找不到该用户信息')
                    else:
                        if user.login_time == payload['data']['login_time']:
                            result = true_return(data=user, msg='请求成功')
                        else:
                            result = false_return(msg='Token已过期')
        else:
            result = false_return(msg='未提供token')
        return result


def auth_required(view_func):
    """
    装饰器，保护需登陆后操作的路由
    :param view_func: 视图函数
    :return:
    """

    @wraps(view_func)
    def wrapper(self):
        result = Auth.identify(self.request)
        if result['success'] and result['data']:
            echo("Token验证成功",flag='SUCCESS')
            self.current_user = result['data']
            view_func(self)
        else:
            echo("Token验证失败: " + result['msg'],flag='ERROR')
            result.update({"token": False})
            self.write(result)

    return wrapper


