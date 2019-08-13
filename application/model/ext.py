from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from application.db_config import SQLITE_DATABASE

engine = create_engine(f'sqlite:///{SQLITE_DATABASE}.db?check_same_thread=False')

Base = declarative_base()

session = sessionmaker(bind=engine)()

import application.model.config
import application.model.blacklist
import application.model.admin

Base.metadata.create_all(engine)
