from arc_logger import log_event
from arc_event_engine import trigger_event
from datetime import datetime

arena_state = {
    "active": False,
    "start_time": None,
    "round": 0
}

def start_arena():

    arena_state["active"] = True
    arena_state["start_time"] = datetime.utcnow().isoformat()
    arena_state["round"] += 1

    log_event("arena_mode", "start_round")

    trigger_event("beat_the_buzzer_arena")

    return {
        "status": "arena_started",
        "round": arena_state["round"],
        "start_time": arena_state["start_time"]
    }


def end_arena():

    arena_state["active"] = False

    log_event("arena_mode", "end_round")

    trigger_event("cross_bay_leaderboard")
    trigger_event("winner_celebration")

    return {
        "status": "arena_finished",
        "round": arena_state["round"]
    }


def get_arena_state():

    return arena_state
