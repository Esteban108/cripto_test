#  TODO : change to read of ENV
SECRET_KEY = "54a1753c3fb214816b3117a82dc4efe0601d293a5804caa64bf529408e14f4fc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DB_URI = "postgresql://postgres:postgres@172.17.0.2:5432/cripto_db"

REDIS_HOST = "172.17.0.4"
REDIS_PORT = 6379
REDIS_DB = 0