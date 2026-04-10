from arc_state import get_state
from arc_logger import log_event

DEAD_ACTIVITY_THRESHOLD = 0
DEAD_ENERGY_THRESHOLD = 2

def detect_dead_time():
    state = get_state()
    presence = state.get("presence", False)
    activity = state.get("activity", 0)
    energy = state.get("energy", 0)

    if not presence:
        return {"status": "no_guests"}

    if activity <= DEAD_ACTIVITY_THRESHOLD and energy <= DEAD_ENERGY_THRESHOLD:
        log_event("dead_time", "room_slowing")
        return {"status": "dead_time_detected"}

    return {"status": "room_active"}
