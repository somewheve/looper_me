from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///looper_me.db?check_same_thread=False')

Base = declarative_base()

session = sessionmaker(bind=engine)()


import application.model.config
import application.model.blacklist
Base.metadata.create_all(engine)
