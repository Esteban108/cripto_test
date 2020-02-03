# coding: utf-8
from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text, Sequence
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import relationship
from api.data_access import Base


#  FOR REAL PROJECTS OR BIG PROJECTS IS BETTER CREATE 1 FILE FOR class

class Coin(Base):
    __tablename__ = 'c_coins'

    description: str = Column(String(200), nullable=False)
    id: str = Column(String(3), primary_key=True)
    created_at: date = Column(Date, nullable=False, index=True)
    status: int = Column(Integer, nullable=False, index=True)


class TransactionType(Base):
    __tablename__ = 'c_transaction_type'

    id: int = Column(Integer, Sequence('seq_transaction_type', metadata=Base.metadata), primary_key=True)
    description: str = Column(String(2044), nullable=False)


class UserType(Base):
    __tablename__ = 'c_user_type'

    id: int = Column(Integer, Sequence('seq_user_type', metadata=Base.metadata), primary_key=True)
    description: str = Column(String(2044), nullable=False)


class User(Base):
    __tablename__ = 'c_user'

    username: str = Column(String(2044), primary_key=True)
    email: str = Column(String(2044), nullable=False, unique=True)
    password: str = Column(Text, nullable=False)
    status: int = Column(Integer, nullable=False, index=True)
    type_id = Column(ForeignKey('c_user_type.id', onupdate='CASCADE', match='FULL'), nullable=False)

    user_type: UserType = relationship('UserType')


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
