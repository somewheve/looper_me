# 全局共享变量


# todo: 集成key设置
# ---->  True标识为未使用
# ----> False标识为已经使用
import tornado.options

variable = {
    "KEY": "fancy",  # 默认的KEY ---> 是可以进行key管理的， 同时key只能被同一个ip进行使用.....
    "AUTH_REQUIRED": True,  # 是否开启key进行校验身份
    "ORIGIN_NUMBER": 1
}
tornado.options.define("variable", default=variable, type=dict)
