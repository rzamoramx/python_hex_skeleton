
from piccolo.engine.postgres import PostgresEngine
from config.constants import (
    DB_SQL_USER,
    DB_SQL_PASSWORD,
    DB_SQL_HOST,
    DB_SQL_PORT,
    DB_SQL_DATABASE,
    DB_SQL_SCHEMA
)


DB = PostgresEngine(
    config={
        "host": DB_SQL_HOST,
        "database": DB_SQL_DATABASE,
        "user": DB_SQL_USER,
        "password": DB_SQL_PASSWORD,
        "port": DB_SQL_PORT,
        "server_settings": {
            "search_path": DB_SQL_SCHEMA
        },
    },
    extensions=(),
)
