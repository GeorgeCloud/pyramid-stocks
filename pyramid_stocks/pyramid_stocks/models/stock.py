from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
)

from .meta import Base


class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    symbol = Column(Text)
    companyName = Column(Text, unique=True)
    description = Column(Text)
    exchange = Column(Text)
    industry = Column(Text)
    website = Column(Text)
    CEO = Column(Text)
    issueType = Column(Text)
    sector = Column(Text)

# Index('symbol_index',)
