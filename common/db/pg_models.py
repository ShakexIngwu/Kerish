from sqlalchemy import (Column, Text, Integer, DateTime, Float, Boolean, ARRAY,
                        Binary, BigInteger, LargeBinary, SmallInteger, Index)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Account(Base):
    __tablename__ = 'app_vol_freq'
    __table_args__ = {'schema': 'api'}

    ddn_name = Column(Text)
    ddn_id = Column(Text, primary_key=True)
    app_node_id = Column(Text, primary_key=True)
    bytes = Column(Float)
    frequency = Column(Integer)
    timestamp = Column(Float)
    log_timestamp = Column(DateTime, primary_key=True)
