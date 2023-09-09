from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean
from db_api.base import Base


class Context(Base):
    __tablename__ = 'context'

    user_id = Column(BigInteger, primary_key=True)
    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String)
    content = Column(String)