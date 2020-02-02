from pydantic import BaseModel


class Status(BaseModel):
    status: str = "Ok"
    detail: str = None


class ClientError(BaseModel):
    status: str = "Fail"
    clear_msg: str = None
    error_msg: str = None


class Token(BaseModel):
    access_token: str
    token_type: str
