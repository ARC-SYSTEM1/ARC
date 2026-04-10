from arc_operator_insight import get_operator_insight
from arc_moment_engine import select_moment


def evaluate_and_act():
    insight = get_operator_insight()
    recommendation = insight.get("reøcommendation")

    moment_result = select_moment()
    selected_moment = moment_result.get("moment")

    if recommendation == "No action needed":
        return {
            "action_taken": "No action needed",
            "moment": None
        }

    if selected_moment:
        return {
            "action_taken": recommendation,
            "moment": selected_moment
        }

    return {
        "action_taken": recommendation,
        "moment": None
    }
