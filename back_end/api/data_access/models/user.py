# coding: utf-8

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from back_end.api.data_access import Base
from .user_type import UserType


class User(Base):
    __tablename__ = 'c_user'

    username: str = Column(String(2044), primary_key=True)
    email: str = Column(String(2044), nullable=False, unique=True)
    password: str = Column(Text, nullable=False)
    status: int = Column(Integer, nullable=False, index=True)
    type_id = Column(ForeignKey('c_user_type.id', onupdate='CASCADE', match='FULL'), nullable=False)

    user_type: UserType = relationship('UserType')
