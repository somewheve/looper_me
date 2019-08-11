import sqlite3


class SqliteClient:
    def __init__(self, db_name, tablename, sql):
        self.conn = sqlite3.connect(db_name + '.db')
        self.tablename = tablename
        self.create(sql)

    def create(self, sql):
        cursor = self.conn.cursor()
        y = cursor.execute(f'select count(*) from sqlite_master where type ="table" and name ="{self.tablename}"')
        if y.fetchone()[0] > 0:
            return
        cursor.execute(sql)
        cursor.close()
        self.conn.commit()

    def query(self, *args, **kwargs):
        """
        usage:
            query( "config_value" , config_name=KEY )
        :param args:
        :param kwargs:
        :return:
        """
        cursor = self.conn.cursor()
        column = ''
        for a in args:
            column += a + ','
        if column.endswith(','): column = column[:-1]
        condition = ''
        for k, v in kwargs.items():
            condition += f'{k}="{v}",'
        if condition: condition = 'where ' + condition
        if condition.endswith(','): condition = condition[:-1]
        sql = f'select {column} from {self.tablename} {condition}'
        res = cursor.execute(sql)
        return res.fetchall()

    def push(self, **kwargs):
        """
        usage :
                push( ip = '127.0.0.1' )
                push( config_name = '', config_value = '' )
        :param args:
        :param kwargs:
        :return:
        """
        column = ''
        for i in list(kwargs.keys()):
            column += i + ','
        if column.endswith(','): column = column[:-1]
        values = tuple(kwargs.values())
        count = ','.join(len(values) * '?')
        cursor = self.conn.cursor()
        sql = f'insert into {self.tablename} ({column}) values ({count})'
        cursor.execute(sql, values)
        cursor.close()
        self.conn.commit()

    def pop(self, **kwargs):
        """
        usage:
              pop( ip = '127.0.0.1' )
        :param args:
        :param kwargs:
        :return:
        """
        cursor = self.conn.cursor()
        cursor.execute(f'delete from {self.tablename} where {list(kwargs.keys())[0]} = "{list(kwargs.values())[0]}"')
        cursor.close()
        self.conn.commit()

    def update(self, **kwargs):
        """
        usage:
                update( config_value = '123456' , condition = 'config_name = "KEY" ' )
        :param args:
        :param kwargs:  condition(可选)
        :return:
        """
        cursor = self.conn.cursor()
        condition = kwargs.pop('condition', '')
        if condition: condition = " where " + condition
        do = ''
        for k, v in kwargs.items():
            do += f'{k}="{v}",'
        if do.endswith(','): do = do[:-1]
        sql = f'update {self.tablename} set {do} {condition}'
        cursor.execute(sql)
        cursor.close()
        self.conn.commit()

    def close(self):
        self.conn.close()

