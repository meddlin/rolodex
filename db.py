import sqlite3

DB_NAME = "database.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                birthday TEXT,
                title TEXT,
                address TEXT,
                notes TEXT,
                tags TEXT
            )
        ''')
        conn.commit()
