import os

from tornado.ioloop import IOLoop
from application import make_app
from application.tcp_server import md_server, trade_server
import application.global_variable

if __name__ == '__main__':
    try:
        md_port = 12572
        md_server.listen(md_port)
        md_server.start()
        td_port = 12472
        trade_server.listen(td_port)
        trade_server.start()
        http_port = 8888
        app = make_app()
        app.listen(http_port)
        os.system(
            f"""echo '数据服务器成功启动^_^ : \n   行情服务器地址---------> tcp://127.0.0.1:{md_port}\n   交易服务器地址---------> tcp://127.0.0.1:{td_port} \n   http服务器-----------> http://127.0.0.1:{http_port}
        '""")

    except Exception as e:
        os.system("echo 启动失败, 请检查端口是否被占用")
    IOLoop.instance().start()
