from arc_autopilot_engine import run_autopilot
from arc_night_replay import log_replay_event
from arc_safety_engine import can_trigger_action, register_action


def execute_autopilot():
    result = run_autopilot()

    status = result.get("status")

    if status != "autopilot_ready":
        log_replay_event("autopilot", status)
        return {
            "status": status,
            "action_taken": None
        }

    selected_moment = result.get("selected_moment")

    safety = can_trigger_action(selected_moment)

    if not safety["allowed"]:
        log_replay_event(
            "autopilot_blocked",
            safety["reason"],
            {
                "selected_moment": selected_moment
            }
        )
        return {
            "status": "blocked",
            "reason": safety["reason"],
            "action_taken": None
        }

    register_action(selected_moment)

    log_replay_event(
        "autopilot",
        "moment_triggered",
        {
            "selected_moment": selected_moment
        }
    )

    return {
        "status": "moment_triggered",
        "action_taken": selected_moment
    }
