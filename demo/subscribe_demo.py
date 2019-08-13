import asyncio
import socket
from threading import Thread


class TransferProtocol:
    """ 解析请求 """
    AUTH_KEY = b"__d41d8cd98f00b204e9800998ecf8427e__"

    def __init__(self, data):
        if isinstance(data, bytes):
            self.data = str(data, encoding="utf-8").replace(self.AUTH_KEY.decode(), "")
        else:
            self.data = data.replace(self.AUTH_KEY, "")
        self.type = None
        self.content = None
        self.auth = False
        self.key = None
        self.parse_result = False
        self._parse()

    def _parse(self):
        """ 解析数据 """
        fancy = self.data.split("--")
        if len(fancy) != 3:
            return
        self.type = fancy[0]
        self.content = fancy[1]
        self.key = fancy[2]
        self.parse_result = True

    def __repr__(self):
        return f"DataProtocol type: {self.type}, content: {self.content}"

    @classmethod
    def create_any(cls, type, data, key):
        return f"{type}--{data}--{key}".encode("utf-8") + cls.AUTH_KEY


class Client:

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, address):
        self.sock.connect(address)
        p = Thread(target=self.recv)
        # p.setDaemon(daemonic=True)
        p.setName("recv")
        p.start()

    def recv(self):
        while True:
            data = self.sock.recv(4096)
            self.process(TransferProtocol(data))

    def process(self, data):
        print(data)

    def subscribe(self, req):
        self.sock.send(req)
        print(self.sock.recv(4096).decode())


if __name__ == '__main__':
    HOST = '10.40.25.18'  # The remote host
    PORT = 12572  # The same port as used by the server
    address = (HOST, PORT)
    client = Client()
    client.connect(address)
    # 服务端分发的密钥
    KEY = "fancy"
    # 发起请求
    req_body = {
        "future_cn": {
            "rb1910.SHFE": ["tick"]
        }
    }
    import json

    req = TransferProtocol.create_any("subscribe", json.dumps(req_body), KEY)
    client.subscribe(req)
