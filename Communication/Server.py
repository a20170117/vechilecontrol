import tornado
import tornado.websocket
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

import json


class WSHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        print(kwargs.pop("context"))
        
        super(WSHandler, self).__init__(application, request, **kwargs)


    def open(self):
        # self.write_message("Hello")
        pass

    def on_message(self, msg):
        # self.write_message("you said: "+msg)
        data = json.loads(msg)
        if data['type'] == 'login':
            ret = self.__check_sessioin(data['session_id'])
            res = {
                'type': 'login',
                'errno': ret
            }
            self.write_message(json.dumps(res))
        elif data['type'] == 'hb':
            # TODO: 更新设备心跳
            pass

    def on_close(self):
        print ("closed")

    def __check_sessioin(self, session_id):
        # TODO: 检查会话是否存在
        # 若是，该会话对应设备状态切换为在线，通知客户端
        # 否则，返回错误
        return 0

class HTTPHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        print(kwargs.pop("context"))
        
        super(HTTPHandler, self).__init__(application, request, **kwargs)

    def get(self):
        pass

    def post(self):
        data = json.loads(self.request.body.decode())

        print(data)

        response = {
            "errno": 0,
            "session_id": "test_session"
        }

        # TODO: 填充response

        self.write(json.dumps(response))

if __name__ == '__main__':

    ctx = "ahahahhahah"
    app = Application([
        (r"/ws",WSHandler, {"context": ctx}),
        (r"/",HTTPHandler, {"context": ctx})
    ])
    server = HTTPServer(app)
    server.listen(8888)
    IOLoop.current().start()