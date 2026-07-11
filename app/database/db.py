import sqlite3
from pathlib import Path

DB_PATH = Path("data/writeoffs.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)

    # Позволяет обращаться к столбцам по имени
    conn.row_factory = sqlite3.Row

    # Включаем поддержку внешних ключей
    conn.execute("PRAGMA foreign_keys = ON")

    return conn