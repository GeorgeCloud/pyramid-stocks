from sqlalchemy.orm import relationship
from .joint import association_table
from .meta import Base

from sqlalchemy import (
    Index,
    Column,
    Integer,
    Text,
)


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
    accounts = relationship(
        'Account',
        secondary=association_table,
        back_populates='stocks'
    )


Index('symbol_index', Stock.symbol, unique=True, mysql_length=255)
