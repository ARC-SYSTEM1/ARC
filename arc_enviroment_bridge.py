import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_LOG_FILE = os.path.join(BASE_DIR, "arc_environment_log.json")


def _ensure_log_file():
    if not os.path.exists(ENV_LOG_FILE):
        with open(ENV_LOG_FILE, "w") as f:
            json.dump([], f)


def _read_log():
    _ensure_log_file()
    try:
        with open(ENV_LOG_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except Exception:
        return []


def _write_log(entries):
    with open(ENV_LOG_FILE, "w") as f:
        json.dump(entries, f, indent=2)


def _record(action_name, message, payload):
    entries = _read_log()
    entries.append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "action": action_name,
        "message": message,
        "payload": payload
    })
    _write_log(entries)


def get_last_environment_event():
    entries = _read_log()
    if not entries:
        return {
            "action": "none",
            "message": "No environment action yet",
            "payload": {}
        }
    return entries[-1]


def trigger_environment_sequence(action_name):
    action_name = str(action_name).lower().strip()

    if action_name == "runner":
        payload = {
            "lights": "runner_blue_flash",
            "sound": "runner_ping",
            "screen": "runner_alert"
        }
        message = "Runner dispatched to dead zone"
        print(f"[ARC ENV] {message}")
        _record("runner", message, payload)
        return {
            "status": "runner",
            "message": message,
            "payload": payload
        }

    elif action_name == "boost":
        payload = {
            "lights": "energy_boost_flash",
            "sound": "energy_rise",
            "screen": "boost_energy"
        }
        message = "Energy boost sequence triggered"
        print(f"[ARC ENV] {message}")
        _record("boost", message, payload)
        return {
            "status": "boost",
            "message": message,
            "payload": payload
        }

    elif action_name == "arena":
        payload = {
            "lights": "arena_red_flash",
            "sound": "arena_hit",
            "screen": "arena_moment"
        }
        message = "Arena moment sequence triggered"
        print(f"[ARC ENV] {message}")
        _record("arena", message, payload)
        return {
            "status": "arena",
            "message": message,
            "payload": payload
        }

    elif action_name == "reset":
        payload = {
            "lights": "standby",
            "sound": "off",
            "screen": "reset"
        }
        message = "Venue reset sequence triggered"
        print(f"[ARC ENV] {message}")
        _record("reset", message, payload)
        return {
            "status": "reset",
            "message": message,
            "payload": payload
        }

    else:
        payload = {}
        message = f"Unknown environment action: {action_name}"
        print(f"[ARC ENV] {message}")
        _record("unknown", message, payload)
        return {
            "status": "unknown",
            "message": message,
            "payload": payload
        }
