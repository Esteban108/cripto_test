from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from back_end.api.depends.depends import get_db
from back_end.api.depends.login_depends import validate_normal_user
from back_end.api.redis_db.operation import get_and_save
from ..operations import OpTransaction, OpCoin
from ..schemas import Transaction, TransactionDB, Coin

router = APIRouter()


@router.get("/transactions_by_user/", response_model=List[TransactionDB], tags=OpTransaction.tags)
def get(skip: int = None, limit: int = None, session: Session = Depends(get_db),
        user_log: dict = Depends(validate_normal_user)):
    data = OpTransaction.op_get_by_user(session, user_log.get("user_name"), skip=skip, limit=limit)
    return data


@router.post("/transaction/", response_model=TransactionDB, tags=OpTransaction.tags)
def create(transaction: Transaction, session: Session = Depends(get_db),
           user_log: dict = Depends(validate_normal_user)):
    #  TODO: ADD VALIDATE: CHECK USER CASH; IF TRANSACTION TYPE IS 2 user_sender_username = NULL else
    #   user_sender_username != NULL
    #   IF transaction type == 3 user_sender == log_user
    ex = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail="Invalid transaction",
    )
    if transaction.user_receiver_username == transaction.user_sender_username:
        raise ex
    transaction_type = OpTransaction.op_get_transaction_type(session, transaction.type_id)
    logged_usr = user_log.get("user_name")

    coin = get_and_save("CACHE_" + transaction.coin_id, OpCoin.op_get, Coin, session, cid=transaction.coin_id)
    if coin.status == 0:
        ex.detail = "Invalid coin"
        raise ex

    if transaction_type is None:
        raise ex
    elif transaction_type.description == "DEBITO":
        if transaction.user_sender_username != logged_usr:
            raise ex
    elif transaction_type.description == "CARGA":
        if transaction.user_receiver_username != logged_usr or transaction.user_sender_username is not None:
            raise ex
    elif transaction_type.description == 'TRANSFERENCIA':
        if transaction.user_sender_username != logged_usr or transaction.user_receiver_username is None:
            raise ex

    return OpTransaction.op_create(session, transaction)
