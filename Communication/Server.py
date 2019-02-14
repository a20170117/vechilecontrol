import tornado
import tornado.websocket
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

import json
import threading
import random
import string
import time
import asyncio


class WSHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        self._ctx = kwargs.pop("context")
        
        super(WSHandler, self).__init__(application, request, **kwargs)


    def open(self):
        # self.write_message("Hello")
        pass

    def on_message(self, msg):
        # self.write_message("you said: "+msg)
        data = json.loads(msg)
        if data['type'] == 'login':
            ret, device = self.__check_sessioin(data['session_id'])
            res = {
                'type': 'login',
                'errno': ret
            }
            self.write_message(json.dumps(res))

            if ret == 0:
                
                self.__start_heartbeat(device)

        elif data['type'] == 'hb':
            # 更新设备心跳
            print(data)
            ret, device = self.__check_sessioin(data['session_id'])
            if ret == 0:
                # 还在线
                device['timeout'] = 0
            pass

    def on_close(self):
        print ("closed")

    @staticmethod
    def heartbeat(handler, device: dict):
        count = 0

        while True:
            hb_msg = {
                'type': 'hb',
                'num': count
            }
            handler.write_message(json.dumps(hb_msg))
            device['hb_list'].append(hb_msg)
            device['timeout'] += 500
            count += 1
            time.sleep(0.5)

            if device['timeout'] > 5000:
                # 超时下线
                handler._ctx['device_list'].remove(device)
                break

    def __start_heartbeat(self, device):
        thr = threading.Thread(target=WSHandler.heartbeat, args=(self, device))
        thr.start()

    def __check_sessioin(self, session_id):
        # 检查会话是否存在
        # 若是，该会话对应设备状态切换为在线，通知客户端，返回(0, 设备对象)
        # 否则，返回(错误编号, None)
        # 错误编号:
        # 0: 正常
        # 1: session_id 不存在

        for device in self._ctx['device_list']:
            if session_id == device['session_id']:
                device['online'] = True
                return 0, device
        return 1, None

class HTTPHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        self._ctx = kwargs.pop("context")
        
        super(HTTPHandler, self).__init__(application, request, **kwargs)

    def get(self):
        pass

    def post(self):
        data = json.loads(self.request.body.decode())

        print(data)

        errno, session_id = self.__create_session(data['device_id'])

        device = {
            'device_id': data['device_id'],
            'session_id': session_id,
            'online': False,
            'timeout': 0,
            'hb_list': []
        }
        self._ctx['device_list'].append(device)
        response = {
            "errno": errno,
            "session_id": session_id
        }

        # TODO: 填充response

        self.write(json.dumps(response))

    def __create_session(self, device_id:str):

        b_flag = True
        while b_flag:
            session_id = ''.join(random.sample(string.ascii_letters + string.digits, 13))

            # 检查session_id是否有冲突
            dev_list = self._ctx['device_list']
            if not dev_list:
                break
            for item in dev_list:
                if item['session_id'] == session_id:
                    b_flag = True
                    break
                b_flag = False

        return 0, session_id

if __name__ == '__main__':

    ctx = {
        "device_list": [],
        "session_timeout": 5000, # ms
    }
    asyncio.set_event_loop(asyncio.new_event_loop())
    app = Application([
        (r"/ws",WSHandler, {"context": ctx}),
        (r"/",HTTPHandler, {"context": ctx})
    ])
    server = HTTPServer(app)
    server.listen(8888)
    IOLoop.current().start()

    li = []
    li.append()