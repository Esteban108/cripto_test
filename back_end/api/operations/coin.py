from sqlalchemy.orm import Session

from ..utils.decorators import sql_errors_controller
from ..data_access.models import Coin as MCoin
from ..schemas import Coin


class Operations:
    __entity_name = "Coins"
    tags = ["Coins"]

    @staticmethod
    @sql_errors_controller
    def op_get(db: Session, cid: str = None, skip=None, limit=None) -> [MCoin]:

        q = db.query(MCoin)

        if cid is not None:
            q = q.filter(MCoin.id == cid)
            return q.one()
        if skip is not None:
            q = q.offset(skip)
        if limit is not None:
            q = q.limit(limit)
        return q.all()

    @staticmethod
    @sql_errors_controller
    def op_create(db: Session, obj: Coin):
        db_obj = MCoin(**obj.dict())

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    @sql_errors_controller
    def op_delete(db: Session, cid: str):
        db.query(MCoin).filter(MCoin.id == cid).delete()
        db.commit()
        return True

    @staticmethod
    @sql_errors_controller
    def op_update(db: Session, obj: Coin):
        db.query(MCoin).filter(MCoin.id == obj.id) \
            .update(obj.dict(exclude={'id'}))
        db.commit()

        return True
