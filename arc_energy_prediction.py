import sqlite3
import time

DB = "arc_events.db"

print("ARC ENERGY PREDICTION RUNNING")

def predict():

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT event, COUNT(*) FROM events GROUP BY event")
    data = cursor.fetchall()

    arrivals = 0
    energy = 0
    activity = 0

    for d in data:

        if d[0] == "arrival":
            arrivals = d[1]

        if d[0] == "energy":
            energy = d[1]

        if d[0] == "activity":
            activity = d[1]

    print("\nARC ENERGY MODEL")

    if arrivals > 5:
        print("Prediction: room likely to become active")

    if energy > activity:
        print("Prediction: energy events dominating")

    if activity > energy:
        print("Prediction: gameplay engagement increasing")

    conn.close()


while True:

    predict()

    time.sleep(60)

