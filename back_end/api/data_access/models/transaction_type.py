# coding: utf-8

from sqlalchemy import Column, Integer, String, Sequence

from back_end.api.data_access import Base


class TransactionType(Base):
    __tablename__ = 'c_transaction_type'

    id: int = Column(Integer, Sequence('seq_transaction_type', metadata=Base.metadata), primary_key=True)
    description: str = Column(String(2044), nullable=False)
