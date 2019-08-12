from application.model.ext import Base, session
from sqlalchemy import Column, Integer, String
import tornado.options


class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(128))
    auth_required = Column(Integer)
    origin_number = Column(Integer)

    col = ['key', 'auth_required', 'origin_number']

    @classmethod
    def load_config(cls):
        res = session.query(cls).first()
        data = {}
        for l in cls.col:
            data[l] = getattr(res, l)
        return data

    @classmethod
    def update(cls, **kwargs):
        model = session.query(cls).first()
        if model:
            for l in cls.col:
                setattr(model, l, kwargs.get(l))

    @classmethod
    def system_start(cls, **kwargs):
        if not session.query(cls).first():
            session.add(Config(**kwargs))
            session.commit()
        else:
            data = cls.load_config()
            for l in cls.col:
                setattr(tornado.options.options, l.upper(), data.get(l))



