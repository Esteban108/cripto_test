# coding: utf-8
from datetime import date

from sqlalchemy import Column, Date, Integer, String

from back_end.api.data_access import Base


class Coin(Base):
    __tablename__ = 'c_coins'

    description: str = Column(String(200), nullable=False)
    id: str = Column(String(3), primary_key=True)
    created_at: date = Column(Date, nullable=False, index=True)
    status: int = Column(Integer, nullable=False, index=True)
