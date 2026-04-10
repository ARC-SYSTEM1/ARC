import time

LAST_AUTOPILOT_ACTION = None
LAST_AUTOPILOT_TIME = 0

COOLDOWN_SECONDS = 120


def can_trigger_action(action_name):
    global LAST_AUTOPILOT_ACTION, LAST_AUTOPILOT_TIME

    if not action_name:
        return {
            "allowed": False,
            "reason": "No action provided"
        }

    now = time.time()

    if LAST_AUTOPILOT_ACTION == action_name and (now - LAST_AUTOPILOT_TIME) < COOLDOWN_SECONDS:
        return {
            "allowed": False,
            "reason": "Same action still in cooldown"
        }

    if (now - LAST_AUTOPILOT_TIME) < COOLDOWN_SECONDS:
        return {
            "allowed": False,
            "reason": "Global autopilot cooldown active"
        }

    return {
        "allowed": True,
        "reason": "Action allowed"
    }


def register_action(action_name):
    global LAST_AUTOPILOT_ACTION, LAST_AUTOPILOT_TIME

    LAST_AUTOPILOT_ACTION = action_name
    LAST_AUTOPILOT_TIME = time.time()

    return {
        "status": "registered",
        "action": action_name,
        "cooldown_seconds": COOLDOWN_SECONDS
    }


def get_safety_status():
    return {
        "last_action": LAST_AUTOPILOT_ACTION,
        "last_action_time": LAST_AUTOPILOT_TIME,
        "cooldown_seconds": COOLDOWN_SECONDS
    }
