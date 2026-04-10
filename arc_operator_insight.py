from arc_dead_zone_engine import detect_dead_zone

PRIORITY_LEVELS = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def get_operator_insight(state, zones):
    decisions = []

    presence = state.get("presence", 0)
    activity = state.get("activity", 0)
    energy = state.get("energy", 0)
    mode = state.get("mode", "STANDBY")

    dead_zone = detect_dead_zone() or {}
    dead = dead_zone.get("dead", False)
    dead_zone_name = dead_zone.get("zone", "venue")

    # 1. Dead zone is the highest operator priority
    if dead:
        decisions.append({
            "primary_action": "Trigger runner",
            "secondary_action": "Boost energy",
            "priority": "high",
            "reason": f"Dead zone detected in {dead_zone_name}",
        })

    # 2. High activity + weak energy = create a moment
    if activity >= 4 and energy <= 4:
        decisions.append({
            "primary_action": "Start arena moment",
            "secondary_action": "Boost energy",
            "priority": "high",
            "reason": "Crowd activity is building but energy is lagging",
        })

    # 3. Low energy with real presence = boost the room
    if presence >= 1 and energy <= 2:
        decisions.append({
            "primary_action": "Boost energy",
            "secondary_action": None,
            "priority": "medium",
            "reason": "Energy levels are low",
        })

    # 4. No presence = reset / standby
    if presence == 0 and activity == 0 and energy == 0:
        decisions.append({
            "primary_action": "Reset venue",
            "secondary_action": None,
            "priority": "medium",
            "reason": "Venue is empty and ready for standby",
        })

    # 5. Strong energy and activity = hold position
    if presence >= 1 and activity >= 3 and energy >= 5:
        decisions.append({
            "primary_action": "No action needed",
            "secondary_action": None,
            "priority": "low",
            "reason": "Venue state is healthy",
        })

    if not decisions:
        return {
            "primary_action": "No action needed",
            "secondary_action": None,
            "priority": "low",
            "reason": "No issues detected",
        }

    decisions = sorted(
        decisions,
        key=lambda d: PRIORITY_LEVELS.get(d.get("priority", "low"), 0),
        reverse=True,
    )

    return decisions[0]
