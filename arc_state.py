import json
import os

STATE_FILE = "/home/chadj0085/ARC/arc_state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {
            "mode": "ACTIVE",
            "presence": 1,
            "activity": 1,
            "energy": 2
        }

    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def get_state():
    return load_state()


def add_energy(amount):
    state = load_state()
    state["energy"] = min(state.get("energy", 0) + amount, 10)
    save_state(state)


def add_activity(amount):
    state = load_state()
    state["activity"] = min(state.get("activity", 0) + amount, 10)
    save_state(state)


def set_arrival():
    state = load_state()
    state["mode"] = "ACTIVE"
    state["presence"] = 1
    save_state(state)


def set_standby():
    state = load_state()
    state["mode"] = "STANDBY"
    state["presence"] = 0
    save_state(state)
