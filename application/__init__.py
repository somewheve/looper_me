import tornado.web

from application.views.blacklist import BlacklistHandler
from application.views.config_manage import ConfigHandler
from application.views.data_manage import DataHandler, DownloadFileHandler
from application.views.ip_manage import IpHandler
from application.views.origin_manage import OriginHandler


def make_app():
    return tornado.web.Application([
        (r"/ip_manage", IpHandler),
        (r'/origin_manage', OriginHandler),
        (r'/blacklist_manage', BlacklistHandler),
        (r'/data_manage', DataHandler),
        (r'/file', DownloadFileHandler),
        (r'/config_manage', ConfigHandler)

    ])
