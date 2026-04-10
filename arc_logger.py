import sqlite3
import datetime

DB = "arc_events.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        value INTEGER,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

def log_event(event_type, value):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    ts = datetime.datetime.now().isoformat()

    c.execute(
        "INSERT INTO events (event_type, value, timestamp) VALUES (?, ?, ?)",
        (event_type, value, ts)
    )

    conn.commit()
    conn.close()

init_db()
