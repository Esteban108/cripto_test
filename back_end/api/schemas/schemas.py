from datetime import date, datetime

from pydantic import BaseModel, EmailStr, validator


class Coin(BaseModel):
    description: str
    id: str
    created_at: date = date.today()
    status: int = 1

    @validator('id')
    def check_username(cls, v):
        if ' ' in v:
            raise ValueError('id not contain a space')
        if len(v) != 3:
            raise ValueError('len of id is 3')
        if v.upper() != v:
            raise ValueError('id is a text in uppercase')
        return v

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
    status: int = 1

    type_id: int = 2

    @validator('username')
    def check_username(cls, v):
        if ' ' in v:
            raise ValueError('username not contain a space')
        return v

    @validator('status')
    def check_status(cls, v):
        if v not in [0, 1]:
            raise ValueError('status only 1(active) or 0(disable)')
        return v

    @validator('type_id')
    def check_type(cls, v):
        if v not in [1, 2]:  # TODO: best read of db and storage in redis for cache
            raise ValueError('status only 1(ADMIN) 2(NORMAL)')
        return v

    class Config:
        orm_mode = True


class UserDB(User):
    email: EmailStr
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

    @validator('type_id')
    def check_type(cls, v):
        if v not in [1, 2, 3]:  # TODO: best read of db and storage in redis for cache
            raise ValueError('status only 1(DEBITO) 2(CARGA) 3(TRANSFERENCIA)')
        return v

    class Config:
        orm_mode = True


class TransactionDB(Transaction):
    id: int
    send_value: str
    coin: Coin
    transaction_type: TransactionType
    user_receiver: User = None
    user_sender: User = None
