def cal_feature(tick) -> object:
    """ 通过传入tick进行计算特征后再返回新的tick"""
    setattr(tick, "ident_feature", str(tick.local_symbol) + str(tick.datetime.timestamp()))
    return tick
