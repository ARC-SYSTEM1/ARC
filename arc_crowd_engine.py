from arc_state import get_state
from arc_logger import log_event

def calculate_crowd_momentum():

    state = get_state()

    presence = state.get("presence", False)
    activity = state.get("activity", 0)
    energy = state.get("energy", 0)

    if not presence:
        momentum = 0

    else:
        momentum = activity + energy

    level = "low"

    if momentum >= 8:
        level = "peak"

    elif momentum >= 5:
        level = "high"

    elif momentum >= 3:
        level = "rising"

    result = {
        "momentum_score": momentum,
        "momentum_level": level
    }

    log_event("crowd_engine", level)

    return result
