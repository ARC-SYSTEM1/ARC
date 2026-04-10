from arc_logger import log_event

def trigger_event(event_type):

    if event_type == "beat_the_buzzer_arena":
        log_event("event_engine", "beat_the_buzzer_arena")
        return {
            "status": "ok",
            "event": "beat_the_buzzer_arena",
            "description": "Arena countdown and buzzer challenge triggered"
        }

    if event_type == "legend_shot_challenge":
        log_event("event_engine", "legend_shot_challenge")
        return {
            "status": "ok",
            "event": "legend_shot_challenge",
            "description": "Legend shot recreation challenge triggered"
        }

    if event_type == "cross_bay_leaderboard":
        log_event("event_engine", "cross_bay_leaderboard")
        return {
            "status": "ok",
            "event": "cross_bay_leaderboard",
            "description": "Cross-bay leaderboard challenge triggered"
        }

    if event_type == "dj_energy_reset":
        log_event("event_engine", "dj_energy_reset")
        return {
            "status": "ok",
            "event": "dj_energy_reset",
            "description": "DJ and lighting reset sequence triggered"
        }

    log_event("event_engine", "unknown")
    return {
        "status": "ok",
        "event": "unknown"
    }
