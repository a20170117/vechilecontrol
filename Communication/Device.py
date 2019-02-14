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
        register_url = 'http://'+self.__config['http_server_addr']+':'+self.__config['http_server_port']+self.__config['http_url']
        post_data = {
            "request": "register",
            "device_id": self.__config['device_id'],
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
        response = json.loads(http_client.fetch(request).body.decode())

        print(response)
        self.__session_id = response['session_id']
        return response['errno']

    def __login(self):
        msg = {
            'type': 'login',
            'device_id': self.__config['device_id'],
            'session_id': self.__session_id
        }

        self.send(msg)

    def on_connection_success(self):
        self.__login()

    def on_connection_close(self, reason):
        print('closed!!!!!!!!!!!!!!!!!!'+' because of '+reason)

    def on_message(self, msg: dict):
        print(msg)
        data = json.loads(msg)
        if data['type'] == 'login':
            # 检查登陆返回值
            if data['errno'] == 0:
                print('login success')
            else:
                print('login failed')
                # 登陆失败，重新注册并登陆
                ret = self.register()
                if ret != 0:
                    # 注册失败
                    raise ValueError
                self.__login()
        elif data['type'] == 'hb':
            data['session_id'] = self.__session_id
            self.send(data)

        return
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

    def connect_ws(self):
        ws_url = 'ws://'+self.__config['ws_server_addr']+':'+self.__config['ws_server_port']+self.__config['ws_url']
        self.connect(ws_url)

if __name__ == '__main__':
    car = Vechile()

    io_loop = ioloop.IOLoop.instance()

    # TODO: 从配置文件中读取
    config = {
        'device_id': 'caterpillar001',
        'http_server_addr': '127.0.0.1',
        'http_server_port': '8888',
        'http_url': '/',
        'ws_server_addr': '127.0.0.1',
        'ws_server_port': '8888',
        'ws_url': '/ws',
        'rtsp_server_addr': '127.0.0.1',
        'rtsp_server_port': 8554
    }

    client = Device(io_loop, car, config)

    result = client.register()

    if result != 0:
        raise ValueError
    else:
        pass

    client.connect_ws()

    try:
        io_loop.start()
    except KeyboardInterrupt:
        client.close()
