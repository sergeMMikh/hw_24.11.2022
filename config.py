import os

TOKEN_TTL = int(os.getenv("TOKEN_TTL", 60 * 60 * 24))

PG_USER = os.getenv("PG_USER", "app")
PG_PASSWORD = os.getenv("PG_PASSWORD", "1234")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", 5433)
PG_DB = os.getenv("PG_DB", "adv_rest_api")

PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
