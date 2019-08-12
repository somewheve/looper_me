import json
from copy import deepcopy
from time import time

import pandas as pd
import tornado.options

from application.global_variable import ORIGIN_NUMBER
from application.tcp_server.helper import DatetimeEncoder
from application.tcp_server.helper import cal_feature
from application.tcp_server.mongo import MotorClient
from application.tcp_server.protocol import DataProtocol


class Buffer:

    def __init__(self, local_symbol, server, size=100):
        self.local_symbol = local_symbol
        self.size = size
        # 过期区域
        self.out_area = set()
        self.server = server
        # 当前正常区域
        self.cur_area = {}
        self.i = 0
        self.motor_client = MotorClient(collection_name=local_symbol)

    @property
    def window(self):
        cur = round(time() * 1000)
        return (cur - self.size, cur, cur + self.size)

    async def push(self, tick):
        tick = cal_feature(tick)
        if tick.ident_feature in self.out_area:
            # or not (self.window[0] < tick.datetime.timestamp() < self.window[1]):
            # 过滤过期数据
            return
        # 推送tick到处理块
        self.cur_area.setdefault(tick.ident_feature, {'count': 0, "data": {}})
        self.cur_area[tick.ident_feature]['count'] += 1
        for key, value in tick._to_dict().items():
            self.cur_area[tick.ident_feature]['data'].setdefault(key, []).append(value)

        # 如果满足的数量已经达到要求 --> 立即进行选举
        if self.cur_area[tick.ident_feature]['count'] >= ORIGIN_NUMBER:
            c = pd.DataFrame(self.cur_area[tick.ident_feature]['data']).set_index(['local_symbol', "datetime"]).groupby(
                level=1).apply(lambda x: x.mode()).dropna()

            res = dict(zip(list(c.columns), list(c.values)[0]))
            res['datetime'] = tick.datetime
            res['local_symbol'] = tick.local_symbol
            # 根据订阅列表进行推送  &&  写入数据库
            ident_feature = deepcopy(res['ident_feature'])
            del res['ident_feature']
            self.i += 1
            if tick.local_symbol in self.server.tick_subscribe_pool.keys():
                for stream in self.server.tick_subscribe_pool[tick.local_symbol]:
                    if not stream.closed():
                        data = DataProtocol.create_any(type="tick_data", data=json.dumps(res, cls=DatetimeEncoder),
                                                       key=tornado.options.options.KEY)
                        await stream.write(data)

            await self.motor_client.insert_one(res)

            # 将特征值记录到过期区中去
            self.out_area.add(ident_feature)

            # 立即回收空间 ---> 优化内存
            self.cur_area.pop(ident_feature, None)
            del ident_feature
            return
