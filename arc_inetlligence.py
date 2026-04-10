import requests
import time

ARC = "http://127.0.0.1:8000"


def get_state():
    return requests.get(f"{ARC}/state", timeout=3).json()


def trigger(endpoint):
    try:
        requests.get(f"{ARC}/{endpoint}", timeout=3)
        print(f"Triggered: {endpoint}")
    except Exception as e:
        print("ARC trigger failed:", e)


while True:
    try:
        state = get_state()

        activity = state["activity"]
        energy = state["energy"]
        mode = state["mode"]

        if activity >= 3 and energy < 3:
            print("Pattern detected: energy spike")
            trigger("energy")

        elif activity == 2 and mode not in ["ARRIVAL", "ENERGY"]:
            print("Pattern detected: active room")
            trigger("activity")

        elif activity == 0 and mode != "STANDBY":
            print("Pattern detected: quiet room")
            trigger("standby")

    except Exception as e:
        print("ARC intelligence error:", e)

    time.sleep(5)

