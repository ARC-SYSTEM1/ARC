from arc_state import get_state
from arc_dead_time import detect_dead_time
from arc_zone_rebalance import get_zone_rebalance

def get_operator_decision():

    state = get_state()
    dead = detect_dead_time()
    rebalance = get_zone_rebalance()

    presence = state.get("presence", False)
    activity = state.get("activity", 0)
    energy = state.get("energy", 0)

    decision = {
        "action": "Maintain Operations",
        "reason": "System stable",
        "severity": "normal",
        "strongest_zone": rebalance.get("strongest_zone"),
        "weakest_zone": rebalance.get("weakest_zone")
    }

    if not presence:
        decision = {
            "action": "Await Guests",
            "reason": "No presence detected",
            "severity": "normal",
            "strongest_zone": None,
            "weakest_zone": None
        }

    elif dead.get("status") == "dead_time_detected":
        decision = {
            "action": "Launch Challenge",
            "reason": "Dead zone detected",
            "severity": "warning",
            "strongest_zone": rebalance.get("strongest_zone"),
            "weakest_zone": rebalance.get("weakest_zone")
        }

    elif rebalance.get("status") == "rebalance_needed":
        decision = {
            "action": "Shift Energy To Weak Zone",
            "reason": "Zone imbalance detected",
            "severity": "warning",
            "strongest_zone": rebalance.get("strongest_zone"),
            "weakest_zone": rebalance.get("weakest_zone")
        }

    elif energy >= 6:
        decision = {
            "action": "Trigger Winner Moment",
            "reason": "Energy spike",
            "severity": "high",
            "strongest_zone": rebalance.get("strongest_zone"),
            "weakest_zone": rebalance.get("weakest_zone")
        }

    elif activity >= 2 and energy >= 3:
        decision = {
            "action": "Maintain Momentum",
            "reason": "Healthy engagement",
            "severity": "good",
            "strongest_zone": rebalance.get("strongest_zone"),
            "weakest_zone": rebalance.get("weakest_zone")
        }

    return decision
