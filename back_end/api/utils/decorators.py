from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from starlette.status import HTTP_400_BAD_REQUEST


def sql_errors_controller(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoResultFound:
            return None
        except IntegrityError as ex:
            if ex.orig.pgcode == '23503':
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail="obj not exist",
                )
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Already exist this obj",
            )

    return inner
