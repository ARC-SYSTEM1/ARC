from arc_state import get_state
import time

moment_history = []

def record_moment_start(moment_name):
    state = get_state()

    event = {
        "moment": moment_name,
        "start_time": time.time(),
        "activity_before": state.get("activity", 0),
        "energy_before": state.get("energy", 0)
    }

    moment_history.append(event)
    return event


def record_moment_result(moment_name, revenue_before, revenue_after):
    state = get_state()

    activity_after = state.get("activity", 0)
    energy_after = state.get("energy", 0)

    for event in reversed(moment_history):
        if event["moment"] == moment_name and "result" not in event:

            event["result"] = {
                "activity_change": activity_after - event["activity_before"],
                "energy_change": energy_after - event["energy_before"],
                "revenue_change": revenue_after - revenue_before
            }

            event["end_time"] = time.time()
            return event

    return {"status": "moment not found"}


def get_outcome_summary():
    completed = [e for e in moment_history if "result" in e]

    if not completed:
        return {"status": "no outcomes recorded"}

    avg_activity = sum(e["result"]["activity_change"] for e in completed) / len(completed)
    avg_energy = sum(e["result"]["energy_change"] for e in completed) / len(completed)
    avg_revenue = sum(e["result"]["revenue_change"] for e in completed) / len(completed)

    return {
        "moments_measured": len(completed),
        "avg_activity_change": avg_activity,
        "avg_energy_change": avg_energy,
        "avg_revenue_change": avg_revenue
    }
