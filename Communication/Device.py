# 网络通信接收指令，转换成虚拟按键码，触发事件
import sys;
sys.path.append(".")
from Events import *
from Vechile import Vechile
from VechileCaterpillarTrack import Caterpillar

from Client import APPLICATION_JSON, WebSocketClient
from VKCode import VK_CODE, VK_MASK
from tornado import gen
from tornado import httpclient
from tornado import httputil
from tornado import ioloop
from tornado import websocket

import functools
import json
import urllib

class Command:
    pass

class Device(WebSocketClient):
    def __init__(self, io_loop, vechile: Vechile, config: dict):
        self.__vechile = vechile
        self.__config = config
        super().__init__(io_loop)

    def register(self):
        headers = httputil.HTTPHeaders({'Content-Type': APPLICATION_JSON})
        register_url = 'http://'+self.__config['http_server_addr']+':'+self.__config['http_server_port']+self.__config['http_register_url']
        post_data = {
            "request": "register",
            "device_id": self.__config['divice_id'],
            "rtsp_server": self.__config['rtsp_server_addr'],
            "rtsp_port": self.__config['rtsp_server_port']
        }
        body = json.dumps(post_data)
        request = httpclient.HTTPRequest(
            url = register_url,
            connect_timeout=self.connect_timeout,
            request_timeout=self.request_timeout,
            headers=headers,
            method="POST",
            body=body
        )
        http_client = httpclient.HTTPClient()
        response = http_client.fetch(request)

        print(response.body)

    def on_connection_success(self):
        pass

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

    # TODO: 从配置文件中读取
    config = {
        'divice_id': 'caterpillar001',
        'http_server_addr': '127.0.0.1',
        'http_server_port': '8888',
        'http_register_url': '/',
        'ws_server_addr': '127.0.0.1',
        'ws_server_port': '8888',
        'rtsp_server_addr': '127.0.0.1',
        'rtsp_server_port': 8554
    }

    client = Device(io_loop, car, config)

    client.register()

    # ws_url = 'ws://127.0.0.1:8888/ws'

    # client.connect(ws_url)

    # try:
    #     io_loop.start()
    # except KeyboardInterrupt:
    #     client.close()
