from arc_environment_controller import environment_action


def run_moment(moment_name):

    if moment_name == "arrival":
        payload = {
            "lights": "soft_on",
            "music": "welcome_track",
            "screens": "welcome_message"
        }

    elif moment_name == "activity":
        payload = {
            "lights": "bright",
            "music": "upbeat",
            "screens": "game_prompt"
        }

    elif moment_name == "energy":
        payload = {
            "lights": "pulse",
            "music": "high_energy",
            "screens": "challenge_prompt"
        }

    elif moment_name == "moment":
        payload = {
            "lights": "flash",
            "music": "arena_hit",
            "screens": "moment_display"
        }

    elif moment_name == "standby":
        payload = {
            "lights": "dim",
            "music": "ambient",
            "screens": "idle_message"
        }

    else:
        payload = {
            "lights": "neutral",
            "music": "none",
            "screens": "none"
        }

    result = environment_action(payload)

    return {
        "moment": moment_name,
        "environment_result": result
    }
