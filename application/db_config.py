MOTOR_ADDRESS = ('localhost', 27017)
MOTOR_DATABASE = 'tick_store'


BLACKLIST_DBNAME='blacklist'
BLACKLIST_TABLENAME = 'blacklist'
BLACKLIST_SQL = f'create table {BLACKLIST_TABLENAME}(id integer primary key autoincrement, ip varchar(20))'

CONFIG_DBNAME='config'
CONFIG_TABLENAME = 'config'
CONFIG_SQL = f'create table {CONFIG_TABLENAME}(id integer primary key autoincrement, config_name varchar(20) UNIQUE,config_value varchar (128))'
