# 网络通信接收指令，转换成虚拟按键码，触发事件
import sys;
sys.path.append(".")
from Events import *
from Vechile import Vechile
from VechileCaterpillarTrack import Caterpillar

from Client import WebSocketClient
from VKCode import VK_CODE, VK_MASK
from tornado import gen
from tornado import httpclient
from tornado import httputil
from tornado import ioloop
from tornado import websocket

import functools
import json

class Command:
    pass

class Device(WebSocketClient):
    def __init__(self, io_loop, vechile: Vechile):
        self.__vechile = vechile
        super().__init__(io_loop)

    def on_message(self, msg: dict):
        command = self.__parse_msg(msg)

        if command['control'] == 'motion':
            code = command['code']
            vechile = self.__vechile
            if code & VK_CODE['w']:
                if code & VK_MASK['depressed']:
                    vechile.event(MoveForward(1.0))
                else:
                    vechile.event(MoveForward(0.0))

            elif code & VK_CODE['s']:
                if code & VK_MASK['depressed']:
                    vechile.event(MoveForward(-1.0))
                else:
                    vechile.event(MoveForward(0.0))

            elif code & VK_CODE['a']:
                if code & VK_MASK['depressed']:
                    vechile.event(MoveRight(-1.0))
                else:
                    vechile.event(MoveRight(0.0))

            elif code & VK_CODE['d']:
                if code & VK_MASK['depressed']:
                    vechile.event(MoveRight(1.0))
                else:
                    vechile.event(MoveRight(0.0))

            elif code & VK_CODE['spacebar']:
                if code & VK_MASK['depressed']:
                    vechile.event(Stop(1.0))
                else:
                    vechile.event(Stop(0.0))

            else:
                print("unknown command code: ", hex(code))

        if command['control'] == 'heart_beat':
            '''
            更新心跳超时时间
            '''
            vechile.event(Stop(0.0))

    def __parse_msg(self, msg):
        command = {
            "control": None,
            "code": 0x120,
            "param": None
        }

        command['control'] = 'motion'

        return command

if __name__ == '__main__':
    car = Vechile()

    io_loop = ioloop.IOLoop.instance()
    client = Device(io_loop, car)
    ws_url = 'ws://127.0.0.1:8888/ws'

    client.connect(ws_url)

    try:
        io_loop.start()
    except KeyboardInterrupt:
        client.close()
