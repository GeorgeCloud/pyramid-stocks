from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    password = Column(Text)
    email = Column(Text)
    username = Column(Text)
