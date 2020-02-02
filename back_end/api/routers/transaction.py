from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from back_end.api.depends.depends import get_db
from back_end.api.depends.login_depends import validate_normal_user
from ..operations import OpTransaction
from ..schemas import Transaction, TransactionDB

router = APIRouter()


@router.get("/transactions_by_user/", response_model=List[TransactionDB], tags=OpTransaction.tags)
def get(skip: int = None, limit: int = None, session: Session = Depends(get_db),
        user_log: dict = Depends(validate_normal_user)):
    data = OpTransaction.op_get_by_user(session, user_log.get("user_name"), skip=skip, limit=limit)
    return data


@router.post("/transaction/", response_model=TransactionDB, tags=OpTransaction.tags)
def create(transaction: Transaction, session: Session = Depends(get_db),
           user_log: dict = Depends(validate_normal_user)):
    if user_log.get("user_name") not in [transaction.user_sender_username, transaction.user_receiver_username]:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Only can create transaction for your user",
        )

    return OpTransaction.op_create(session, transaction)
