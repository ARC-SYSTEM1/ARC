# ARC Venue Configuration Layer
# Allows ARC to run different venues with different settings

VENUE_CONFIG = {
    "venue_id": "arc_demo_001",

    "venue_type": "social_sports",

    "zones": [
        "court_a",
        "court_b",
        "bar",
        "lounge"
    ],

    "thresholds": {
        "low_energy": 40,
        "high_energy": 75,
        "low_activity": 20
    },

    "moments_enabled": [
        "engagement",
        "challenge",
        "arena_mode"
    ],

    "autopilot_enabled": True
}


def get_venue_config():
    return VENUE_CONFIG


def get_threshold(name):
    return VENUE_CONFIG["thresholds"].get(name)


def get_zones():
    return VENUE_CONFIG["zones"]


def autopilot_enabled():
    return VENUE_CONFIG["autopilot_enabled"]
