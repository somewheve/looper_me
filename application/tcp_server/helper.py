import json
from datetime import datetime, date


def cal_feature(tick) -> object:
    """ 通过传入tick进行计算特征后再返回新的tick"""
    setattr(tick, "ident_feature", str(tick.local_symbol) + str(tick.datetime.timestamp()))
    return tick


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
