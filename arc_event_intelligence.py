import sqlite3
import time

DB = "arc_events.db"

print("ARC EVENT INTELLIGENCE RUNNING")

def analyze():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT event, COUNT(*) FROM events GROUP BY event")
    results = cursor.fetchall()

    print("\n--- ARC EVENT SUMMARY ---")

    for r in results:
        print(r[0], ":", r[1])

    conn.close()


while True:

    analyze()

    time.sleep(30)

