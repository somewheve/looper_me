import tornado.web
import tornado.options


class BaseHandle(tornado.web.RequestHandler):
    def set_default_headers(self):
        # 后面的*可以换成ip地址，意为允许访问的地址
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type,Content-Length, Authorization, Accept,X-Requested-With')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE,OPTIONS')
        self.set_header('Access-Control-Expose-Headers', 'Content-Disposition')

    def options(self):
        self.set_status(200)
        self.finish()
