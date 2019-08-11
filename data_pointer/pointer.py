# 数据焦点
import socket
from threading import Thread
from typing import Tuple

from ctpbee import CtpbeeApi, dumps
from ctpbee.constant import ContractData, BarData, SharedData, TickData, LogData, PositionData, TradeData, OrderData, \
    AccountData

from data_pointer.constant import EVENT_TICK, AUTH_KEY


class TcpClient:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._active = True

    def connect(self, address: Tuple):
        self.socket.connect(address)

    def send(self, message: bytes):
        self.socket.send(message)

    def monitoro_message(self):
        while True:
            recv = self.socket.recv(4096)
            print(str(recv, encoding="utf-8"))

    def _after_connect(self):
        p = Thread(target=self.monitoro_message)
        p.setDaemon(daemonic=True)
        p.start()


class DataPointer(CtpbeeApi):

    def __init__(self, name, looper_address: Tuple, key):
        super().__init__(extension_name=name)
        self.client = TcpClient()
        self.client.connect(looper_address)
        self.key = key

    def on_contract(self, contract: ContractData):
        self.app.subscribe(contract.symbol)

    def on_shared(self, shared: SharedData) -> None:
        pass

    def on_bar(self, bar: BarData) -> None:
        # sel
        pass

    def on_tick(self, tick: TickData) -> None:
        p = dumps(tick)
        fancy = EVENT_TICK + "--" + p + "--" + self.key
        p = bytes(fancy, encoding="utf-8") + AUTH_KEY
        self.client.send(p)

    def on_log(self, log: LogData):
        pass

    def on_position(self, position: PositionData) -> None:
        pass

    def on_trade(self, trade: TradeData) -> None:
        pass

    def on_order(self, order: OrderData) -> None:
        pass

    def on_account(self, account: AccountData) -> None:
        pass
