from application.model.ext import Base, session
from sqlalchemy import Column, Integer, String
from werkzeug.security import check_password_hash, generate_password_hash
import time


class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(32), unique=True, default=lambda: time.time().hex())
    username = Column(String(32), unique=True)
    _password = Column('password', String(128))
    login_time = Column(Integer)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd):
        self._password = generate_password_hash(pwd)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    def update_password(self, old, new):
        if self.check_password(old):
            self.password = new
            session.commit()
            return True
        return False

    @classmethod
    def system_start(cls):
        res = session.query(cls).first()
        if res: return
        session.add(cls(username='admin', password='123456'))
        session.commit()
