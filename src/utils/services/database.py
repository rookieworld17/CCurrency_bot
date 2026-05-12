import sqlite3
from typing import Optional
from utils.cfg.config import DB_PATH
from datetime import datetime, timezone
import os

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            language TEXT NOT NULL DEFAULT 'EN'
        )
    ''')

    for column, definition in [
        ("username", "TEXT"),
        ("last_interaction", "DATETIME"),
    ]:
        try:
            cursor.execute(f"ALTER TABLE users ADD COLUMN {column} {definition}")
        except sqlite3.OperationalError:
            pass

    conn.commit()
    conn.close()

# ========== USERS ==========

def add_user(tg_id: int, username: Optional[str] = None):
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT OR IGNORE INTO users (user_id, username, last_interaction) VALUES (?, ?, ?)',
            (tg_id, username, now)
        )
        cursor.execute(
            'UPDATE users SET username = ?, last_interaction = ? WHERE user_id = ?',
            (username, now, tg_id)
        )
        conn.commit()
    finally:
        conn.close()

def get_language(tg_id: int) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT language FROM users WHERE user_id = ?', (tg_id,))
        row = cursor.fetchone()
        return row[0] if row else 'EN'
    finally:
        conn.close()

def set_language(tg_id: int, lang: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE users SET language = ? WHERE user_id = ?', (lang, tg_id))
        conn.commit()
    finally:
        conn.close()
