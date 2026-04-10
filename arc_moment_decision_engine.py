from arc_state import get_state
from arc_dead_time_engine import detect_dead_time
from arc_crowd_engine import calculate_crowd_momentum

def choose_moment():

    state = get_state()
    dead = detect_dead_time()
    crowd = calculate_crowd_momentum()

    activity = state.get("activity",0)
    energy = state.get("energy",0)
    momentum = crowd.get("momentum_level","low")

    scores = {}

    scores["legend_shot_challenge"] = activity + (1 if momentum == "rising" else 0)

    scores["beat_the_buzzer_arena"] = energy + (2 if momentum == "high" else 0)

    scores["arena_round"] = energy + activity

    scores["dj_energy_reset"] = 5 if dead.get("status") == "dead_time_detected" else 0

    best = max(scores, key=scores.get)

    return {
        "scores": scores,
        "chosen_moment": best
    }
