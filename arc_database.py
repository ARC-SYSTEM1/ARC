import sqlite3
import time

DB = "arc_events.db"

def init_db():
    conn = sqlite3.connect(DB, check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        event TEXT,
        activity INTEGER,
        energy INTEGER,
        presence BOOLEAN
    )
    """)

    conn.commit()
    conn.close()

def log_event(event, activity, energy, presence):
    conn = sqlite3.connect(DB, check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO events (timestamp,event,activity,energy,presence) VALUES (?,?,?,?,?)",
        (time.strftime("%H:%M:%S"), event, activity, energy, presence)
    )

    conn.commit()
    conn.close()

init_db()
