import sqlite3
DB="database/healthcare.db"

def get_conn():
    return sqlite3.connect(DB)
