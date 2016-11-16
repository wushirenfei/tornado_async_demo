# -*- coding=utf-8 -*-
from tornado import httpserver, ioloop, options, web
from tornado import gen
from tornado.options import define, options

define(name='port', default=8080, help='run on given port', type=int)
from tornado.gen import Task

class IndexHandler(web.RequestHandler):

    @gen.coroutine
    def get(self):
        yield gen.sleep(1)
        self.write('python.org'*20)

if __name__ == '__main__':
    options.parse_command_line()
    app = web.Application(handlers=[(r'/index', IndexHandler)])
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()
