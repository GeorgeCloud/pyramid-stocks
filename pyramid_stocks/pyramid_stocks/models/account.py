from .meta import Base
from datetime import datetime as dt
from sqlalchemy.exc import DBAPIError
from cryptacular import bcrypt
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
    Boolean
)

manager = bcrypt.BCRYPTPasswordManager()


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    password = Column(Text)
    email = Column(Text)
    username = Column(Text)
    registered_on = Column(DateTime, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)

    def __init__(self, email, username, password, admin=False):
        self.email = email
        self.username = username
        self.password = manager.encode(password, 10)
        self.registered_on = dt.now()
        self.admin = admin

    @classmethod
    def check_credentials(cls, request=None, username=None, password=None):
        if request.dbsession is None:
            raise DBAPIError
        is_authenticated = False
        query = request.dbsession.query(cls).filter(
            cls.username == username).one_or_none()
        if query is not None:
            if manager.check(query.password, password):
                is_authenticated = True

        return (is_authenticated, username)


# query = request.dbsession.query(cls)
# return(manager.check(query.password, password), username)
