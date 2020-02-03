from datetime import datetime, timedelta

import jwt

from ..config import SECRET_KEY, ALGORITHM, MINUTES_TO_EXPIRE


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=MINUTES_TO_EXPIRE)
    to_encode.update({"exp": datetime.timestamp(expire)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
