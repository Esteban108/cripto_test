from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from ..data_access.models import Transaction
from ..data_access.models import User as MUser
from ..schemas import User, UserDB


class Operations:
    __entity_name = "Users"
    tags = ["Users"]

    @staticmethod
    def op_get(db: Session, user_name: str):
        q = db.query(MUser).filter(MUser.username == user_name)
        return q.one()

    @staticmethod
    def op_create(db: Session, obj: UserDB):
        db_obj = MUser(**obj.dict())

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def op_delete(db: Session, user_name: str):
        db.query(MUser).filter(MUser.username == user_name).delete()
        db.commit()
        return True

    @staticmethod
    def op_update(db: Session, obj: User):
        db.query(MUser).filter(MUser.username == obj.username) \
            .update(obj.dict(exclude={'user_type', 'username'}))
        db.commit()

        return True

    """
    @staticmethod
    def op_login(db: Session, cred: Credentials):
        usr: MUser = db.query(MUser).filter(MUser.email == cred.email) \
            .filter(MUser.password == cred.password).filter(MUser.status == 1).one()
        if not usr:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"user_name": usr.username, "user_type": usr.user_type.description},
                                           expires_delta=access_token_expires)

        return {"access_token": access_token, "token_type": "bearer"}
    
    @staticmethod
    def op_validate_token(token: str, user_type_valid: [str]):
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
            if token_data.get("user_type") not in user_type_valid:
                raise credentials_exception
            return True
        except PyJWTError:
            raise credentials_exception
    """

    @staticmethod
    def get_balance(db: Session, user_name):
        q_positives = db.query(Transaction.coin_id, func.sum(Transaction.send_value).label("total")) \
            .filter(Transaction.user_receiver_username == user_name) \
            .group_by(Transaction.coin_id)
        q_negatives = db.query(Transaction.coin_id, func.sum(Transaction.send_value).label("total")) \
            .filter(Transaction.user_sender_username == user_name) \
            .group_by(Transaction.coin_id)

        positives = q_positives.all()
        negatives = q_negatives.all()
        global_balance: {"coin_id": "balance"} = {}
        for row in positives:
            coin_balance = global_balance.get(row.coin_id, 0)
            global_balance.update({row.coin_id: coin_balance + row.total})

        for row in negatives:
            coin_balance = global_balance.get(row.coin_id, 0)
            global_balance.update({row.coin_id: coin_balance - row.total})

        return global_balance
