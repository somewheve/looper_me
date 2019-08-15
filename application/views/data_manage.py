"""
data views ----->
后台管理 data视图函数
"""
from datetime import datetime

from application.views import BaseHandle
from application.common import true_return, false_return, echo
from application.tcp_server.mongo import MotorClient
from application.views.auth import coroutine_auth_required
import pandas as pd


async def filter(collection: list, start: datetime = None, end: datetime = None):
    """
    :param collection:
    :param start:
    :param end:
    :return:
            data = {
                    'zn1908.SHFE':[{},{}],
                    'zn1909.SHFE':[{},{},{}],
                    }
    """
    data = {}
    for colle in collection:
        """  对应条件查询 """
        motor_client = MotorClient(collection_name=colle)
        if start and end:
            condition = {"datetime": {'$gte': start, '$lte': end}}
        elif start:
            condition = {"datetime": {'$gte': start}}
        elif end:
            condition = {"datetime": {'$lte': end}}
        else:
            condition = {}
        cursor = motor_client.collection.find(condition).sort('datetime')
        async for document in cursor:
            try:
                document['datetime'] = datetime.strftime(document['datetime'], '%Y-%m-%d %H:%M:%S')
            except KeyError:
                document['datetime'] = datetime.strftime(document['datetime'], '%Y-%m-%d %H:%M:%S.%f')
            document.pop('_id', None)
        data[colle] = document
        # data[colle] = [document async for document in cursor if document.pop('_id', None) or 1]
    return data


class DataHandler(BaseHandle):
    @coroutine_auth_required
    async def get(self):
        motor_client = MotorClient()
        collections = await motor_client.get_collections()
        data = []
        for i in collections:
            data.append({'name': i})
        self.write(true_return(data=data))


class DownloadFileHandler(BaseHandle):
    @coroutine_auth_required
    async def post(self):
        code = self.get_argument('code')
        start = self.get_argument('start', None)
        end = self.get_argument('end', None)
        csv = self.get_argument('csv', None)
        filename = ''
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

        echo(type(code), code)

        """ 过滤查询 """
        results = await filter(code, start, end)

        if csv:
            """dataframe 处理 """
            df = pd.DataFrame()
            for k, v in results.items():
                df = pd.DataFrame(v, index=[k] * len(v))
            # df == Dataframe
            data_csv = f" ,{str(list(df)).replace('[', '').replace(']', '')}"
            for row in df.itertuples():
                temp = str(list(row)).replace('[', '').replace(']', '')
                data_csv += '{},\r\n'.format(temp)
        else:
            """ 处理 """
            data_csv = ''
            for k, v in results.items():
                data_csv += '{},\r\n'.format(k)
                for item in v:
                    item = str(item).replace('{', '').replace('}', '')
                    data_csv += '{},\r\n'.format(item)
        """写入"""
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'filename={}'.format(filename.encode('utf-8').decode('ISO-8859-1')))
        self.write(data_csv)
        self.finish()
