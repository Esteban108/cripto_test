from datetime import datetime

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from starlette.status import HTTP_401_UNAUTHORIZED

from back_end.api.utils.token import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


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
    if user["user_type"] != "ADMIN":
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="You do haven't access to this resource",
        )
    return user


def validate_normal_user(user: dict = Depends(op_validate_token)):
    if user["user_type"] not in ["ADMIN", "NORMAL"]:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="You do haven't access to this resource",
        )
    return user
