from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_422_UNPROCESSABLE_ENTITY

from back_end.api.depends.depends import get_db
from back_end.api.depends.login_depends import validate_normal_user, validate_admin
from ..operations import OpUser
from ..schemas import User, UserDB, Status, Token
from ..utils.hash import pwd_context

router = APIRouter()

""" IS NOT NECESSARY
@router.get("/users/{user_name}", response_model=User, tags=OpUser.tags)
def get(user_name: str, session: Session = Depends(get_db), user_log: dict = Depends(validate_normal_user)):
    data = OpUser.op_get(session, user_name)
    return data
"""


@router.get("/user/balance", tags=OpUser.tags)
def get(session: Session = Depends(get_db), user_log: dict = Depends(validate_normal_user)):
    data = OpUser.get_balance(session, user_log.get("user_name"))
    return data


@router.post("/user/", response_model=User, tags=OpUser.tags)
def create(user: UserDB, session: Session = Depends(get_db)):
    user.password = pwd_context.hash(user.password)
    if user.type_id != 2:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only can create normal user",
        )
    return OpUser.op_create(session, user)


@router.post("/user_admin/", response_model=User, tags=OpUser.tags)
def create2(user: UserDB, session: Session = Depends(get_db), user_log: dict = Depends(validate_admin)):
    user.password = pwd_context.hash(user.password)
    return OpUser.op_create(session, user)


@router.put("/user/", response_model=Status, tags=OpUser.tags)
def update(user: User, session: Session = Depends(get_db), user_log: dict = Depends(validate_normal_user)):
    s = Status()
    if user.username != user_log.get("user_name"):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Only can update your user",
        )
    if not OpUser.op_update(session, user):
        s.status = "Fail"
    return s


@router.delete("/user/", response_model=Status, tags=OpUser.tags)
def delete(session: Session = Depends(get_db), user_log: dict = Depends(validate_normal_user)):
    s = Status()  # TODO ADD desactivate user
    if not OpUser.op_delete(session, user_log.get("user_name")):
        s.status = "Fail"
    return s


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    token = OpUser.op_login(session, form_data.username, form_data.password)
    if not token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token
