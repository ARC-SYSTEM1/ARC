import json
import os
from datetime import datetime

REPLAY_FILE = os.path.expanduser("~/ARC/arc_night_replay_log.json")


def _ensure_replay_file():
    if not os.path.exists(REPLAY_FILE):
        with open(REPLAY_FILE, "w") as f:
            json.dump([], f)


def _load_events():
    _ensure_replay_file()
    try:
        with open(REPLAY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def _save_events(events):
    with open(REPLAY_FILE, "w") as f:
        json.dump(events, f, indent=2)


def log_replay_event(event_type, value, extra=None):
    events = _load_events()

    event = {
        "time": datetime.utcnow().isoformat(),
        "event": event_type,
        "value": value
    }

    if extra and isinstance(extra, dict):
        event.update(extra)

    events.append(event)
    _save_events(events)

    return event


def get_night_replay(limit=25):
    events = _load_events()
    return events[-limit:]


def get_night_summary(limit=25):
    events = get_night_replay(limit)

    summary = []
    for e in events:
        summary.append({
            "time": e.get("time", "Unknown time"),
            "event": e.get("event", "unknown"),
            "value": e.get("value", "unknown")
        })

    return {
        "events_reviewed": len(events),
        "replay": summary
    }


def clear_night_replay():
    _save_events([])
    return {"status": "cleared"}


if __name__ == "__main__":
    print(get_night_summary())
