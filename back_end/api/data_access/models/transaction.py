# coding: utf-8
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Sequence
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import relationship

from back_end.api.data_access import Base
from .coin import Coin
from .transaction_type import TransactionType
from .user import User


class Transaction(Base):
    __tablename__ = 'c_transaction'

    send_value: MONEY = Column(MONEY, nullable=False)
    date: datetime = Column(DateTime(True), nullable=False, index=True)
    id: int = Column(Integer, Sequence('seq_transaction', metadata=Base.metadata), primary_key=True)
    coin_id = Column(ForeignKey('c_coins.id', onupdate='CASCADE', match='FULL'), nullable=False, index=True)
    user_sender_username = Column(ForeignKey('c_user.username', onupdate='CASCADE', match='FULL'), index=True)
    user_receiver_username = Column(ForeignKey('c_user.username', onupdate='CASCADE', match='FULL'), index=True)
    type_id = Column(ForeignKey('c_transaction_type.id', onupdate='CASCADE', match='FULL'), nullable=False, index=True)

    coin: Coin = relationship('Coin')
    transaction_type: TransactionType = relationship('TransactionType')
    user_receiver: User = relationship('User', primaryjoin='Transaction.user_receiver_username == User.username')
    user_sender: User = relationship('User', primaryjoin='Transaction.user_sender_username == User.username')
