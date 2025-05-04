import os

import psycopg
from dotenv import load_dotenv

# Load .env once at import time
load_dotenv()


def get_conn() -> psycopg.Connection:
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "openair"),
        user=os.getenv("DB_USER", "air"),
        password=os.getenv("DB_PASSWORD", ""),
        autocommit=False,
    )
