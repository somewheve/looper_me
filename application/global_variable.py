# 全局共享变量


# todo: 集成key设置
# ---->  True标识为未使用
# ----> False标识为已经使用
import tornado.options

KEY = "fancy"  # 默认的KEY ---> 是可以进行key管理的， 同时key只能被同一个ip进行使用.....
AUTH_REQUIRED = 1  # 1 | 0 是否开启key进行校验身份
ORIGIN_NUMBER = 1

tornado.options.define("KEY", default=KEY, type=str)
tornado.options.define("AUTH_REQUIRED", default=True, type=bool)
tornado.options.define("ORIGIN_NUMBER", default=ORIGIN_NUMBER, type=int)