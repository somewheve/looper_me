from functools import lru_cache
from hashlib import md5


@lru_cache(maxsize=100000)
def cal_md(string):
    return md5(string.encode()).hexdigest()


def cal_feature(tick) -> object:
    """ 通过传入tick进行计算特征后再返回新的tick"""
    if tick.symbol == "ag1910":
        print(tick.datetime)
        print(tick.datetime.timestamp())
    setattr(tick, "ident_feature", str(tick.local_symbol) + str(tick.datetime.timestamp()))
    return tick
