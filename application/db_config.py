MOTOR_ADDRESS = ('localhost', 27017)
MOTOR_DATABASE = 'tick_store'

BLACKLIST_DBNAME = 'blacklist'
BLACKLIST_TABLENAME = 'blacklist'
BLACKLIST_SQL = f'create table {BLACKLIST_TABLENAME}(id integer primary key autoincrement, ip varchar(20))'

CONFIG_DBNAME = 'config'
CONFIG_TABLENAME = 'config'
CONFIG_SQL = f'create table {CONFIG_TABLENAME}(id integer primary key autoincrement, KEY varchar(56) unique ,AUTH_REQUIRED integer unique ,ORIGIN_NUMBER integer unique )'
