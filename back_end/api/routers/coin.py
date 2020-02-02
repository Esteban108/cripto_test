from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from back_end.api.depends.login_depends import validate_normal_user, validate_admin
from ..operations import OpCoin
from ..schemas import Coin, Status
from back_end.api.depends.depends import get_db
from typing import Union

router = APIRouter()


@router.get("/coins/", response_model=Union[List[Coin], Coin], tags=OpCoin.tags)
def get(coin_id: str = None, skip: int = None, limit: int = None, session: Session = Depends(get_db),
        user_log: dict = Depends(validate_normal_user)):
    data = OpCoin.op_get(session, coin_id, skip=skip, limit=limit)
    return data


@router.post("/coin/", response_model=Coin, tags=OpCoin.tags)
def create(coin: Coin, session: Session = Depends(get_db), user_log: dict = Depends(validate_admin)):
    return OpCoin.op_create(session, coin)


@router.delete("/coin/{coin_id}", response_model=Status, tags=OpCoin.tags)
def delete(coin_id: str, session: Session = Depends(get_db), user_log: dict = Depends(validate_admin)):
    status = Status()
    if OpCoin.op_delete(session, coin_id):
        return status
