from arc_state import get_state
from arc_logger import log_event

def get_night_flow():
    state = get_state()

    presence = state.get("presence", False)
    activity = state.get("activity", 0)
    energy = state.get("energy", 0)

    if not presence:
        phase = "arrival"
        action = "wait_for_guests"

    elif activity <= 1 and energy <= 2:
        phase = "warmup"
        action = "build_energy"

    elif activity >= 2 and energy >= 3 and energy < 6:
        phase = "engage"
        action = "run_challenges"

    elif energy >= 6 and energy < 8:
        phase = "arena"
        action = "launch_arena_mode"

    else:
        phase = "peak"
        action = "trigger_celebration"

    result = {
        "phase": phase,
        "action": action,
        "state": state
    }

    log_event("night_flow", phase)
    return result
