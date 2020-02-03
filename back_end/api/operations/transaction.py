from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from back_end.api.utils.decorators import sql_errors_controller
from .user import Operations as user_op
from ..data_access.models import Transaction as MTransaction
from ..data_access.models import TransactionType
from ..schemas.schemas import Transaction


class Operations:
    __entity_name = "Transaction"
    tags = ["Transaction"]

    @staticmethod
    @sql_errors_controller
    def op_get_by_user(db: Session, user_name: str, skip: int = None, limit: int = None) -> [MTransaction]:
        q = db.query(MTransaction).filter(
            or_(user_name == MTransaction.user_sender_username, user_name == MTransaction.user_receiver_username))
        if skip is not None:
            q = q.offset(skip)
        if limit is not None:
            q = q.limit(limit)

        return q.all()

    @staticmethod
    @sql_errors_controller
    def op_create(db: Session, obj: Transaction) -> MTransaction:

        if obj.user_sender_username is not None:  # if transaction_type is None: transaction_type = Deposito
            balance = user_op.get_balance(db, obj.user_sender_username)
            if balance[obj.coin_id] < obj.send_value:
                raise HTTPException(400, f"not have money for this transaction")

        db_obj = MTransaction(**obj.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    @sql_errors_controller
    def op_get_transaction_type(db: Session, t_id: int) -> TransactionType:
        return db.query(TransactionType).filter(t_id == TransactionType.id).one()

    """  # I NOT NEED THIS METHODS
    @staticmethod
    def op_delete(db: Session, transaction_id: int):
        db.query(MTransaction).filter(MTransaction.id == transaction_id).delete()
        db.commit()
        return True

    @staticmethod
    def op_update(db: Session, obj: User):
        db.query(UserDB).filter(UserDB.username == obj.username) \
            .update(obj.dict(exclude={'user_type', 'username'}))
        db.commit()

        return True
    """
