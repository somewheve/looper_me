from ctpbee import CtpBee

from data_pointer.pointer import DataPointer

if __name__ == '__main__':
    """ 简单的基于ctpbee的数据发送端 """
    app = CtpBee("data_pointer", __name__)
    app.config.from_json("data_pointer/config.json")
    pointer = DataPointer("origin_pointer", ("127.0.0.1", 12572), "fancy")
    app.add_extension(pointer)
    app.start()
