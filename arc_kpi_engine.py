from arc_state import get_state

def get_kpi_metrics():
    state = get_state()

    presence = bool(state.get("presence", False))
    activity = int(state.get("activity", 0) or 0)
    energy = int(state.get("energy", 0) or 0)
    mode = state.get("mode", "UNKNOWN")

    guests_present = max(1, activity * 4) if presence else 0

    if activity >= 3 and energy >= 3:
        conversion_signal = "high"
    elif activity >= 1 or energy >= 1:
        conversion_signal = "medium"
    else:
        conversion_signal = "low"

    if not presence:
        alert_level = "idle"
    elif energy == 0 and activity == 0:
        alert_level = "watch"
    else:
        alert_level = "normal"

    system_health = "healthy"
    moment_trigger_count = activity + energy
    replay_events_logged = moment_trigger_count * 3

    return {
        "guests_present": guests_present,
        "activity_score": activity,
        "energy_score": energy,
        "conversion_signal": conversion_signal,
        "alert_level": alert_level,
        "system_health": system_health,
        "mode": mode,
        "moment_trigger_count": moment_trigger_count,
        "replay_events_logged": replay_events_logged
    }
