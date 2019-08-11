import tornado.options

from data_pointer.constant import AUTH_KEY


class DataProtocol:
    """ 解析请求 """

    def __init__(self, data):
        if isinstance(data, bytes):
            self.data = str(data, encoding="utf-8").replace(AUTH_KEY.decode(), "")
        else:
            self.data = data.replace(AUTH_KEY, "")
        self.type = None
        self.content = None
        self.auth = False
        self.key = None
        self.parse_result = False
        self._parse()
        self.auth_required()

    def _parse(self):
        """ 解析数据 """
        fancy = self.data.split("--")
        if len(fancy) != 3:
            return
        self.type = fancy[0]
        self.content = fancy[1]
        self.key = fancy[2]
        self.parse_result = True

    def auth_required(self):
        """ 装饰器 """
        if not self.parse_result:
            # 解析失败
            return
        if self.key == tornado.options.options.KEY:
            self.auth = True

    @classmethod
    def create_any(cls, type, data, key):
        return f"{type}--{data}--{key}".encode("utf-8") + AUTH_KEY

    def __repr__(self):
        return f"DataProtocol type: {self.type}, content: {self.content}"
