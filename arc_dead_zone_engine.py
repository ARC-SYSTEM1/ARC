from arc_state import get_state


def detect_dead_zone():
    state = get_state()

    presence = state.get("presence", False)
    activity = state.get("activity", 0)
    energy = state.get("energy", 0)

    result = {
        "zone": None,
        "dead": False,
        "reason": "stable"
    }

    # No guests at all
    if not presence:
        return {
            "zone": "venue",
            "dead": False,
            "reason": "no_guests_present"
        }

    # Bar dead-zone logic
    if presence and activity >= 1 and energy < 25:
        return {
            "zone": "bar",
            "dead": True,
            "reason": "bar_energy_drop"
        }

    # Arena dead-zone logic
    if presence and activity < 2 and energy < 30:
        return {
            "zone": "arena",
            "dead": True,
            "reason": "low_activity_low_energy"
        }

    # Venue-wide softness
    if presence and activity < 1 and energy < 20:
        return {
            "zone": "venue",
            "dead": True,
            "reason": "venue_stall"
        }

    return result
