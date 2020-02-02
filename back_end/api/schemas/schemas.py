from datetime import date, datetime

from pydantic import BaseModel, EmailStr


class Coin(BaseModel):
    description: str
    id: str
    created_at: date = date.today()
    status: int = 1

    class Config:
        orm_mode = True


class TransactionType(BaseModel):
    description: str

    class Config:
        orm_mode = True


class UserType(BaseModel):
    description: str

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    email: EmailStr
    status: int = 1

    type_id: int

    class Config:
        orm_mode = True


class UserDB(User):
    password: str


class Credentials(BaseModel):
    email: EmailStr
    password: str


class Transaction(BaseModel):
    send_value: int
    date: datetime = datetime.now()
    coin_id: str
    type_id: int
    user_sender_username: str = None
    user_receiver_username: str = None

    class Config:
        orm_mode = True


class TransactionDB(Transaction):
    id: int
    send_value: str
    coin: Coin
    transaction_type: TransactionType
    user_receiver: User = None
    user_sender: User = None
