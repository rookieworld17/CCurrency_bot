import sqlite3
from src.config import DB_PATH
import os

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# ========== USERS ==========

def add_user(tg_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (tg_id,))
        conn.commit()
    finally:
        conn.close()

def get_subscribe(tg_id: int) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT subscribe FROM users WHERE user_id = ?', (tg_id,))
        return cursor.fetchone()[0]
    finally:
        conn.close()

def set_subscribe(tg_id: int, status: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE users SET subscribe = ? WHERE user_id = ?', (status, tg_id))
        conn.commit()
    finally:
        conn.close()