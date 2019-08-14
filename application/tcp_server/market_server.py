import asyncio
import json

from ctpbee import loads
from application.common import echo
from application.model import blacklist_db
from application.tcp_server.buffer import Buffer
from application.tcp_server.constant import REPLY, REQ_TYPE, REQ_SUB, REQ_DATA, REQ_TICK
from application.tcp_server.fancy import CoreServer
from application.logger import logger


class MarketServer(CoreServer):
    def __init__(self):
        super().__init__()
        # 全局stream对象
        self.global_connection = {}

        # 黑名单
        self.blacklist = blacklist_db.load_ip()

        self.tick_origin = set()
        self.buffers = {}

        # tick 订阅池子
        self.tick_subscribe_pool = {}

        self.funcs = {}

        # 缓冲区
        self.buffer = dict()

        # 注册相应的处理事件
        self._register_handle_func()

    def connection_made(self, address, stream):
        s = address[0] + ":" + str(address[1])
        if s in self.blacklist:
            stream.close()
            return
        self.global_connection[s] = stream
        echo(f'{address} connected!', falg='INFO')

    def connection_lost(self, address: tuple, exception):
        pass

    def _register_handle_func(self):
        self.funcs = {
            REQ_SUB: self.subscribe,
            REQ_DATA: self.process_data_req,
            REQ_TICK: self.process_tick
        }

    async def process_tick(self, **kwargs):
        tick_data = kwargs.get("content")
        tick = loads(tick_data)

        if tick.local_symbol not in self.buffers:
            self.buffers[tick.local_symbol] = Buffer(tick.local_symbol, self)
        await asyncio.wait_for(self.buffers[tick.local_symbol].push(tick), timeout=1)

    async def process_data_req(self, **kwargs):
        """ 处理数据请求 """
        pass

    async def process_bar(self, **kwargs):
        pass

    async def subscribe(self, **kwargs):
        # 发起订阅请求
        # todo 校验身份 ---> 通过校验的KEY来确认身份
        address = kwargs.get("address")
        stream = kwargs.get("stream")
        # 获取期货订阅
        data = kwargs.get("content")
        sub_data = json.loads(data)
        # 期货订阅代码
        future_cn = sub_data.get("future_cn")
        for key, value in future_cn.items():
            if "tick" in value:
                self.tick_subscribe_pool.setdefault(key, []).append(stream)

    async def handler(self, type, content, stream, address):
        if type not in REQ_TYPE:
            pass
        if type == 'tick':
            self.tick_origin.add(address[0] + ":" + str(address[1]))
        await self.funcs[type](content=content, stream=stream, address=address)
        await stream.write(REPLY['success'])
