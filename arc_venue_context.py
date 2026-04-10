venues = {}

def get_venue_context(venue_id="default"):

    if venue_id not in venues:
        venues[venue_id] = {
            "state": {
                "mode": "STANDBY",
                "presence": False,
                "activity": 0,
                "energy": 0
            },
            "events": [],
            "replay": []
        }

    return venues[venue_id]


def list_venues():
    return list(venues.keys())
