from copy import deepcopy
from time import time

from application.global_variable import ORIGIN_NUMBER
from application.tcp_server.helper import cal_feature
from application.tcp_server.mongo import MotorClient


class Buffer:

    def __init__(self, local_symbol, server, size=100):
        self.local_symbol = local_symbol
        self.size = size
        # 过期区域
        self.out_area = set()
        self.server = server
        # 当前正常区域
        self.cur_area = {}
        self.motor_client = MotorClient(collection_name=local_symbol)

    @property
    def window(self):
        cur = round(time() * 1000)
        return (cur - self.size, cur, cur + self.size)

    async def push(self, tick):
        if tick.ident_feature in self.out_area:
            # or not (self.window[0] < tick.datetime.timestamp() < self.window[1]):
            # 过滤过期数据
            return
        # 推送tick到源
        self.cur_area.setdefault(tick.ident_feature, {'count': 0, "data": []})
        self.cur_area[tick.ident_feature]['count'] += 1
        self.cur_area[tick.ident_feature].append(tick)

        # 如果满足的数量已经达到要求 --> 立即进行选举

        if self.cur_area[tick.ident_feature]['count'] >= ORIGIN_NUMBER:
            result = sorted(self.cur_area[tick.ident_feature]['data'].items(), key=lambda item: len(item[1])).pop()
            res = result[1][0]
            # 根据订阅列表进行推送  &&  写入数据库
            ident_feature = deepcopy(res.ident_feature)
            delattr(res, 'ident_feature')
            delattr(res, 'data_feature')
            # if res.symbol == 'zn1910':
            #     await self.motor_client.find()
            if res.symbol == "zn1910":
                print(res)
            await self.motor_client.insert_one(res._to_dict())
            for stream in self.server.subscribed_pool.values():
                await stream.write(res)

            # 将特征值记录到过期区中去
            self.out_area.add(ident_feature)

            # 立即回收空间 ---> 优化内存
            self.cur_area.pop(ident_feature, None)
            del ident_feature
