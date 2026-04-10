def evaluate_decision(state):
    presence = state.get("presence", 0)
    activity = state.get("activity", 0)
    energy = state.get("energy", 0)

    # DEAD ZONE (no activity, low energy)
    if presence and activity < 2 and energy < 25:
        return {
            "action": "engagement_moment",
            "reason": "dead_zone_detected"
        }

    # LOW ENERGY
    elif presence and energy < 40:
        return {
            "action": "energy_boost",
            "reason": "low_energy"
        }

    # CROWD BUILDING → NEED MOMENT
    elif presence and activity >= 5 and energy <= 40:
        return {
            "action": "arena_moment",
            "reason": "crowd_building_energy_low"
        }

    # HIGH ENERGY → PUSH MOMENT
    elif presence and activity >= 5 and energy >= 70:
        return {
            "action": "arena_moment",
            "reason": "high_energy"
        }

    # ACTIVE ROOM → REVENUE MOMENT
    elif presence and activity >= 2:
        return {
            "action": "revenue_prompt",
            "reason": "active_guests_detected"
        }

    # EMPTY VENUE
    elif presence == 0:
        return {
            "action": "reset_venue",
            "reason": "venue_empty"
        }

    # DEFAULT
    return {
        "action": "none",
        "reason": "stable"
    }
