from api.data_access import SessionLocal
from fastapi.security import OAuth2PasswordBearer


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


"""
def auth(user_type: [str], www_authenticate: str = Header(None)):
    try:
        return Operations().op_validate_token(www_authenticate, user_type)
    except HTTPException as ex:
        raise ex
"""

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
