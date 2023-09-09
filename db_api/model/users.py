from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean
from db_api.base import Base


class Users(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    calendar_id = Column(String, default='')