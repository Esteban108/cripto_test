#  TODO : change to read of ENV
SECRET_KEY = "54a1753c3fb214816b3117a82dc4efe0601d293a5804caa64bf529408e14f4fc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
MINUTES_TO_EXPIRE = 15

DB_URI = "postgresql://postgres:postgres@cripto_postgres:5432/cripto_db"

REDIS_HOST = "cripto_redis"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_CACHE_TIME = 60 * 10
