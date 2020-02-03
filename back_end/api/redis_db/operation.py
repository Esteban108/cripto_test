import json

from back_end.api.config import REDIS_CACHE_TIME
from . import R


def get_and_save(key, callable=None, pydanic_model=None, *args, **kwargs):
    value = R.get(key)
    if value is None and callable is not None:
        value = callable(*args, **kwargs)
        if value is not None:
            if pydanic_model is not None:
                value = pydanic_model.from_orm(value)
                R.setex(key, REDIS_CACHE_TIME, value.json())
            else:
                R.setex(key, REDIS_CACHE_TIME, value)
    else:
        value = json.loads(value)
        if pydanic_model is not None:
            value = pydanic_model(**value)

    return value
