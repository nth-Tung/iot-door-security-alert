import sqlite3

DB_PATH = 'database.db'

def get_all_receivers():
    """Trả về list email người nhận dạng [(name, email), ...]"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT name, email FROM receivers')
    rows = c.fetchall()
    conn.close()
    return rows
