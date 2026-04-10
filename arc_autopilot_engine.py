from arc_dead_zone_engine import detect_dead_zone
from arc_moment_engine import select_moment
from arc_operator_override import get_override_status


def run_autopilot():
    override = get_override_status()

    if not override["autopilot_enabled"]:
        return {
            "status": "autopilot_disabled"
        }

    if override["override_active"]:
        return {
            "status": "override_active",
            "forced_action": override["forced_action"]
        }

    dead_zone = detect_dead_zone()

    if not dead_zone.get("dead_zone"):
        return {
            "status": "idle",
            "reason": "No dead zone detected"
        }

    if override["forced_action"]:
        return {
            "status": "autopilot_ready",
            "selected_moment": override["forced_action"],
            "recommendation": "Forced operator action"
        }

    moment = select_moment()
    selected = moment.get("moment")

    if not selected:
        return {
            "status": "no_moment_selected",
            "reason": "No valid moment available"
        }

    return {
        "status": "autopilot_ready",
        "dead_zone": dead_zone,
        "selected_moment": selected,
        "recommendation": moment.get("recommendation", "")
    }
