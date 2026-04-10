from arc_state import get_state
from arc_dead_time_engine import detect_dead_time
from arc_zone_rebalance import get_zone_rebalance
from arc_crowd_engine import calculate_crowd_momentum
from arc_moment_engine import trigger_moment
from arc_event_engine import trigger_event
from arc_moment_decision_engine import choose_moment
from arc_logger import log_event

def run_moment_autopilot():
    state = get_state()
    presence = state.get("presence", False)
    activity = state.get("activity", 0)
    energy = state.get("energy", 0)

    if not presence:
        log_event("moment_autopilot", "idle_no_guests")
        return {"moment_autopilot": "idle"}

    dead = detect_dead_time()
    rebalance = get_zone_rebalance()
    crowd = calculate_crowd_momentum()
    level = crowd.get("momentum_level", "low")

    if dead.get("status") == "dead_time_detected":
        result = trigger_event("dj_energy_reset")
        log_event("moment_autopilot", "dj_energy_reset")
        return {"moment_autopilot": "dj_energy_reset", "result": result}

    if rebalance.get("status") == "rebalance_needed":
        result = trigger_event("cross_bay_leaderboard")
        log_event("moment_autopilot", "cross_bay_leaderboard")
        return {"moment_autopilot": "cross_bay_leaderboard", "result": result}

    decision = choose_moment()
    chosen = decision['chosen_moment']

    if chosen == 'winner_celebration' or level == "peak" or energy >= 8:
        result = trigger_moment("winner_celebration")
        log_event("moment_autopilot", "winner_celebration")
        return {"moment_autopilot": "winner_celebration", "result": result}

    if level == "high" or (activity >= 2 and energy >= 4):
        result = trigger_event("beat_the_buzzer_arena")
        log_event("moment_autopilot", "beat_the_buzzer_arena")
        return {"moment_autopilot": "beat_the_buzzer_arena", "result": result}

    if level == "rising" or (activity >= 1 and energy >= 3):
        result = trigger_event("legend_shot_challenge")
        log_event("moment_autopilot", "legend_shot_challenge")
        return {"moment_autopilot": "legend_shot_challenge", "result": result}

    log_event("moment_autopilot", "maintain")
    return {"moment_autopilot": "maintain"}
