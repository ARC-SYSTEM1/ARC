import time
from datetime import datetime

from arc_action_engine import evaluate_and_act
from arc_state import get_state
from arc_night_replay import log_replay_event


LAST_ACTION = None
LAST_ACTION_TIME = 0
COOLDOWN_SECONDS = 30


def should_trigger(action_name: str) -> bool:
    global LAST_ACTION, LAST_ACTION_TIME

    if not action_name or action_name == "No action needed":
        return False

    now = time.time()

    if LAST_ACTION == action_name and (now - LAST_ACTION_TIME) < COOLDOWN_SECONDS:
        return False

    LAST_ACTION = action_name
    LAST_ACTION_TIME = now
    return True


def run_pulse():

    state = get_state()

    energy = state.get("energy", 0)
    activity = state.get("activity", 0)

    result = evaluate_and_act()

    action_taken = result.get("action_taken")

    # Log the pulse event
    log_replay_event(
        "pulse",
        action_taken,
        {
            "energy": energy,
            "activity": activity
        }
    )

    if not should_trigger(action_taken):
        return {
            "status": "no_action",
            "action_taken": action_taken,
            "energy": energy,
            "activity": activity,
            "timestamp": datetime.utcnow().isoformat()
        }

    return {
        "status": "action_triggered",
        "action_taken": action_taken,
        "energy": energy,
        "activity": activity,
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    print("ARC Pulse Runner started")

    while True:
        result = run_pulse()
        print(result)
        time.sleep(10)
