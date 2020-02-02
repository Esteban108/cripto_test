from datetime import datetime
from datetime import timedelta

from api.config import ACCESS_TOKEN_EXPIRE_MINUTES
from api.data_access.models import User as MUser
from api.utils.hash import pwd_context
from api.utils.token import create_access_token, decode_token
from fastapi import HTTPException, Depends
from jwt import PyJWTError
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from starlette.status import HTTP_401_UNAUTHORIZED

from .depends import oauth2_scheme


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


def op_validate_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if token is None:
            raise credentials_exception

        token_data = decode_token(token)
        date_to_expire = datetime.fromtimestamp(token_data.get("exp"))
        if datetime.now() > date_to_expire:
            raise credentials_exception
        #    if token_data.get("user_type"):
        #        raise credentials_exception
        return {"user_name": token_data.get("user_name"), "user_type": token_data.get("user_type")}
    except PyJWTError:
        raise credentials_exception


def validate_admin(user: dict = Depends(op_validate_token)):
    if user["user_type"] != "admin":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="You do haven't access to this resource",
        )
    return user


def validate_normal_user(user: dict = Depends(op_validate_token)):
    if user["user_type"] not in ["admin", "normal"]:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="You do haven't access to this resource",
        )
    return user
