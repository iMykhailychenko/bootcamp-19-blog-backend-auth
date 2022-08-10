import os

POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_DB = os.getenv("POSTGRES_DB", "bc-19-blog")
POSTGRES_USER = os.getenv("POSTGRES_USER", "bootcamp")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "1234")

SECRET_KEY = os.getenv("SECRET_KEY", "asdfasdf")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "21000"))
