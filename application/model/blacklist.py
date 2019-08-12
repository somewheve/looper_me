from application.model.ext import Base, session
from sqlalchemy import Column, Integer, String


class Blacklist(Base):
    __tablename__ = 'blacklist'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(32))

    @classmethod
    def load_ip(cls):
        res = session.query(cls).all()
        data = set()
        for i in res:
            data.add(i.ip)
        return data

    @classmethod
    def add(cls, ip):
        session.add(Blacklist(ip=ip))
        session.commit()

    @classmethod
    def delete(cls, ip):
        model = session.query(cls).filter_by(ip=ip).first()
        if model:
            session.delete(model)
            session.commit()
