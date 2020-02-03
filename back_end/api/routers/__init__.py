from .coin import router as con
from .transaction import router as trn
from .user import router as usr

routers = [usr, con, trn]
