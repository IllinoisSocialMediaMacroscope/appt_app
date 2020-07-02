import sqlite3
from flask import current_app, g

def get_db():
    conn = g._database = sqlite3.connect('appt_tracker.db')
    conn.execute('''PRAGMA foreign_keys = 1''')
    conn.row_factory = sqlite3.Row

    return conn