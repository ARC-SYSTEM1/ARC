def run_environment(moment_type):

    if moment_type == "challenge":
        return {
            "lights": "spotlight",
            "music": "challenge_cue",
            "screens": "challenge_graphic",
            "status": "environment_triggered"
        }

    elif moment_type == "celebration":
        return {
            "lights": "flash",
            "music": "celebration_hit",
            "screens": "winner_graphic",
            "status": "environment_triggered"
        }

    elif moment_type == "energy_boost":
        return {
            "lights": "pulse",
            "music": "energy_rise",
            "screens": "hype_graphic",
            "status": "environment_triggered"
        }

    elif moment_type == "reset":
        return {
            "lights": "neutral",
            "music": "ambient",
            "screens": "reset_graphic",
            "status": "environment_triggered"
        }

    elif moment_type == "finale":
        return {
            "lights": "arena_full",
            "music": "finale_theme",
            "screens": "finale_graphic",
            "status": "environment_triggered"
        }

    else:
        return {
            "status": "unknown_environment_moment"
        }
