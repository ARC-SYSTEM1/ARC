import random
from arc_dead_zone_engine import detect_dead_zone


def select_moment():
    zone_status = detect_dead_zone()

    if not zone_status["dead_zone"]:
        return {
            "moment": None,
            "reason": "No engagement intervention needed"
        }

    severity = zone_status["severity"]

    low_energy_moments = [
        "challenge_mode",
        "cross_bay_challenge",
        "quick_shootout"
    ]

    medium_energy_moments = [
        "arena_mode",
        "energy_boost",
        "music_reset"
    ]

    if severity == "high":
        moment = random.choice(low_energy_moments)

    elif severity == "medium":
        moment = random.choice(medium_energy_moments)

    else:
        moment = None

    return {
        "moment": moment,
        "severity": severity,
        "recommendation": zone_status["recommendation"]
    }
