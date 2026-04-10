import time
import json
import os

STATE_FILE = "/home/chadj0085/ARC/arc_state.json"
MEMORY_FILE = "/home/chadj0085/ARC/arc_memory.json"
EVENT_LOG = "/home/chadj0085/ARC/arc_events.json"
PERF_FILE = "/home/chadj0085/ARC/arc_performance.json"

COOLDOWN_SECONDS = 10


# -------------------------
# FILE HELPERS
# -------------------------
def load_json(path, default):
    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
    except:
        pass
    return default


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f)


# -------------------------
# STATE
# -------------------------
def get_state():
    return load_json(
        STATE_FILE,
        {"mode": "STANDBY", "presence": 0, "activity": 0, "energy": 0}
    )


def update_state(state):
    save_json(STATE_FILE, state)


# -------------------------
# MEMORY
# -------------------------
def load_memory():
    return load_json(
        MEMORY_FILE,
        {
            "current_mode": None,
            "mode_step": 0,
            "last_action_time": 0,
            "last_action": None
        }
    )


def save_memory(memory):
    save_json(MEMORY_FILE, memory)


# -------------------------
# PERFORMANCE TRACKING
# -------------------------
def update_performance(action, delta_energy):
    perf = load_json(PERF_FILE, {})

    if action not in perf:
        perf[action] = {
            "count": 0,
            "total_gain": 0,
            "avg_gain": 0
        }

    perf[action]["count"] += 1
    perf[action]["total_gain"] += delta_energy
    perf[action]["avg_gain"] = perf[action]["total_gain"] / perf[action]["count"]

    save_json(PERF_FILE, perf)


# -------------------------
# MODE LOGIC
# -------------------------
def select_mode(state):
    energy = state["energy"]
    activity = state["activity"]
    presence = state["presence"]

    if presence == 0:
        return None
    if energy <= 2:
        return "energy_recovery"
    if 3 <= energy <= 5:
        return "engagement_build"
    if energy >= 6:
        return "hype"
    return None


MODES = {
    "energy_recovery": ["reset", "engage", "boost", "arena"],
    "engagement_build": ["engage", "boost", "arena"],
    "hype": ["celebrate", "arena"]
}


# -------------------------
# ACTION EFFECTS
# -------------------------
def apply_action_effect(action, state):
    state = dict(state)

    if action == "reset":
        state["activity"] = max(0, state["activity"] - 1)

    elif action == "engage":
        state["activity"] += 1

    elif action == "boost":
        state["energy"] += 1

    elif action == "arena":
        state["energy"] += 2
        state["activity"] += 1

    elif action == "celebrate":
        state["energy"] += 1

    # clamp
    state["energy"] = max(0, min(state["energy"], 10))
    state["activity"] = max(0, min(state["activity"], 10))

    return state


# -------------------------
# LOOP
# -------------------------
def cooldown(memory):
    return (time.time() - memory["last_action_time"]) < COOLDOWN_SECONDS


def loop():
    print("[ARC CORE + LEARNING] running")

    while True:
        try:
            state = get_state()
            memory = load_memory()

            if cooldown(memory):
                time.sleep(2)
                continue

            # MODE
            if not memory["current_mode"]:
                memory["current_mode"] = select_mode(state)
                memory["mode_step"] = 0

            mode = memory["current_mode"]

            if not mode:
                time.sleep(3)
                continue

            sequence = MODES.get(mode, [])
            step = memory["mode_step"]

            if step >= len(sequence):
                memory["current_mode"] = None
                memory["mode_step"] = 0
                save_memory(memory)
                continue

            action = sequence[step]

            print(f"[ACTION] {action}")

            before = dict(state)
            after = apply_action_effect(action, state)

            delta_energy = after["energy"] - before["energy"]

            update_state(after)
            update_performance(action, delta_energy)

            memory["last_action"] = action
            memory["last_action_time"] = time.time()
            memory["mode_step"] += 1
            save_memory(memory)

            print(f"[LEARN] {action} → Δenergy={delta_energy}")

            time.sleep(3)

        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(5)


if __name__ == "__main__":
    loop()
