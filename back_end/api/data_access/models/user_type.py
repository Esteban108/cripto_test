# coding: utf-8

from sqlalchemy import Column, Integer, String, Sequence

from back_end.api.data_access import Base


#  FOR REAL PROJECTS OR BIG PROJECTS IS BETTER CREATE 1 FILE FOR class

class UserType(Base):
    __tablename__ = 'c_user_type'

    id: int = Column(Integer, Sequence('seq_user_type', metadata=Base.metadata), primary_key=True)
    description: str = Column(String(2044), nullable=False)
