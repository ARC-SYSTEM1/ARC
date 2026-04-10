from arc_state import get_state
from arc_logger import log_event

def detect_dead_time():
    state = get_state()

    presence = state.get("presence", False)
    activity = state.get("activity", 0)
    energy = state.get("energy", 0)

    if presence and activity == 0 and energy <= 2:
        log_event("dead_time", "critical_idle")
        return {
            "status": "dead_time_detected",
            "severity": "high",
            "reason": "presence_true_activity_zero_energy_low"
        }

    if presence and activity <= 1 and energy <= 2:
        log_event("dead_time", "low_engagement")
        return {
            "status": "dead_time_detected",
            "severity": "medium",
            "reason": "presence_true_low_activity_low_energy"
        }

    log_event("dead_time", "clear")
    return {
        "status": "clear",
        "severity": "none",
        "reason": "activity_or_energy_ok"
    }
