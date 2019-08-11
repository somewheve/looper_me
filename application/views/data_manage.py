"""
data views ----->
后台管理 data视图函数
"""
from datetime import datetime

from application.views import BaseHandle
from application.common import true_return, false_return
from application.tcp_server.mongo import MotorClient


async def filter(collection: list, start: datetime = None, end: datetime = None, download: bool = False):
    data = []
    for colle in collection:
        """分隔每个种类"""
        if download:
            data.append(colle)
        """  对应条件查询 """
        motor_client = MotorClient(collection_name=colle)
        if start and end:
            cursor = motor_client.collection.find({"datetime": {'$gte': start, '$lte': end}}).sort('datetime')
            data.extend([document async for document in cursor if document.pop('_id', None) or 1])
            continue
        elif start:
            cursor = motor_client.collection.find({"datetime": {'$gte': start}}).sort('datetime')
            data.extend([document async for document in cursor if document.pop('_id', None) or 1])
            continue
        elif end:
            cursor = motor_client.collection.find({"datetime": {'$lte': end}}).sort('datetime')
            data.extend([document async for document in cursor if document.pop('_id', None) or 1])
            continue
        else:
            cursor = motor_client.collection.find()
            data.extend([document async for document in cursor if document.pop('_id', None) or 1])
    return data


class DataHandler(BaseHandle):
    async def get(self):
        motor_client = MotorClient()
        collections = await motor_client.get_collections()
        data = []
        for i in collections:
            data.append({'name': i})
        self.write(true_return(data=data))

    async def post(self):
        pass
        # todo:查看
        # code = self.get_argument('code')
        # start = self.get_argument('start', None)
        # end = self.get_argument('end', None)
        # """ 检查参数,转换"""
        # if not code:
        #     return
        # code = code.split('+')
        # try:
        #     if start:
        #         start = datetime.strptime(start, '%Y-%m-%d')
        #     if end:
        #         end = datetime.strptime(end, '%Y-%m-%d')
        # except ValueError:
        #     self.write(false_return(msg='日期参数格式错误'))
        #     return
        # """过滤查询"""
        # res = await filter(code, start, end)
        # self.write(true_return(data=res))


class DownloadFileHandler(BaseHandle):
    async def post(self):
        code = self.get_argument('code')
        start = self.get_argument('start', None)
        end = self.get_argument('end', None)
        filename = ''
        data_csv = ''
        """ 检查参数,转换参数,设定文件名"""
        if not code:
            return
        code = code.split('+')
        try:
            if start:
                filename += start + "_"
                start = datetime.strptime(start, '%Y-%m-%d')
            if end:
                filename += end + "_"
                end = datetime.strptime(end, '%Y-%m-%d')
        except ValueError:
            self.write(false_return(msg='日期参数格式错误'))
            return
        filename = '{}{}.csv'.format(filename, code[0] if len(code) == 1 else 'Many')

        print(type(code), code)
        """ 过滤查询 """
        results = await filter(code, start, end, download=True)
        """ 处理 """
        for item in results:
            if isinstance(item, dict):
                try:
                    print(item['datetime'])
                    item['datetime'] = datetime.strftime(item['datetime'], '%Y-%m-%d %H:%M:%S')
                except KeyError:
                    item['datetime'] = datetime.strftime(item['datetime'], '%Y-%m-%d %H:%M:%S.%f')
            item = str(item).replace('{', '').replace('}', '')
            data_csv += '{},\r\n'.format(item, )
        """写入"""
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'filename={}'.format(filename.encode('utf-8').decode('ISO-8859-1')))
        self.write(data_csv)
        self.finish()
