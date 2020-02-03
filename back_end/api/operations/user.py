from datetime import timedelta

from sqlalchemy import Numeric, cast
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func

from back_end.api.config import ACCESS_TOKEN_EXPIRE_MINUTES
from back_end.api.utils.decorators import sql_errors_controller
from back_end.api.utils.hash import pwd_context
from back_end.api.utils.token import create_access_token
from ..data_access.models import Transaction, User as MUser
from ..schemas import User, UserDB


class Operations:
    __entity_name = "Users"
    tags = ["Users"]

    @staticmethod
    @sql_errors_controller
    def op_get(db: Session, user_name: str):
        q = db.query(MUser).filter(MUser.username == user_name)
        return q.one()

    @staticmethod
    @sql_errors_controller
    def op_create(db: Session, obj: UserDB):
        db_obj = MUser(**obj.dict())

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    @sql_errors_controller
    def op_delete(db: Session, user_name: str):
        db.query(MUser).filter(MUser.username == user_name).delete()
        db.commit()
        return True

    @staticmethod
    @sql_errors_controller
    def op_update(db: Session, obj: User):
        db.query(MUser).filter(MUser.username == obj.username) \
            .update(obj.dict(exclude={'user_type', 'username'}))
        db.commit()

        return True

    @staticmethod
    def op_login(db: Session, email: str, password: str):
        try:
            usr: MUser = db.query(MUser).filter(MUser.email == email).filter(MUser.status == 1).one()
        except NoResultFound:
            return None

        if not usr or not pwd_context.verify(password, usr.password):
            return None
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"user_name": usr.username, "user_type": usr.user_type.description},
                                           expires_delta=access_token_expires)

        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    @sql_errors_controller
    def get_balance(db: Session, user_name):
        q_positives = db.query(Transaction.coin_id, cast(func.sum(Transaction.send_value), Numeric).label("total")) \
            .filter(Transaction.user_receiver_username == user_name) \
            .group_by(Transaction.coin_id)
        q_negatives = db.query(Transaction.coin_id, cast(func.sum(Transaction.send_value), Numeric).label("total")) \
            .filter(Transaction.user_sender_username == user_name) \
            .group_by(Transaction.coin_id)

        positives = q_positives.all()
        negatives = q_negatives.all()
        global_balance: {"coin_id": "balance"} = {}
        for row in positives:
            coin_balance = global_balance.get(row.coin_id, 0)
            global_balance.update({row.coin_id: coin_balance + row.total})

        for row in negatives:
            coin_balance = global_balance.get(row.coin_id, 0)
            global_balance.update({row.coin_id: coin_balance - row.total})

        return global_balance
