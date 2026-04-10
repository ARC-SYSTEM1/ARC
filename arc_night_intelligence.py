from arc_end_of_day import get_end_of_day
from arc_roi_engine import get_roi_metrics
from arc_kpi_engine import get_kpi_metrics


def get_night_intelligence():
    end_day = get_end_of_day()
    roi = get_roi_metrics()
    kpi = get_kpi_metrics()

    revenue = end_day.get("revenue_today", 0)
    profit = end_day.get("profit_today", 0)
    roi_percent = end_day.get("roi_percent", 0)
    activity = end_day.get("activity_score", 0)
    energy = end_day.get("energy_score", 0)
    orders = end_day.get("orders_today", 0)

    if revenue == 0:
        revenue_read = "No revenue generated"
    elif revenue < 50:
        revenue_read = "Low revenue night"
    elif revenue < 200:
        revenue_read = "Moderate revenue night"
    else:
        revenue_read = "Strong revenue night"

    if energy == 0:
        energy_read = "No energy activity"
    elif energy < 3:
        energy_read = "Low energy"
    elif energy < 6:
        energy_read = "Moderate energy"
    else:
        energy_read = "High energy"

    if activity == 0:
        activity_read = "Room stayed quiet"
    elif activity < 3:
        activity_read = "Light room activity"
    elif activity < 6:
        activity_read = "Moderate room activity"
    else:
        activity_read = "High room activity"

    if roi_percent < 0:
        recommendation = "Increase traffic or reduce operating cost"
    elif roi_percent < 40:
        recommendation = "Improve conversion and raise spend per guest"
    elif roi_percent < 100:
        recommendation = "Stable night, continue optimizing"
    else:
        recommendation = "Strong night, repeat this operating pattern"

    score = 50
    score += min(orders * 3, 15)
    score += min(activity * 4, 15)
    score += min(energy * 4, 15)
    if roi_percent > 0:
        score += 15
    if roi_percent > 40:
        score += 10
    if roi_percent > 100:
        score += 10
    score = max(0, min(score, 100))

    return {
        "night_score": score,
        "revenue_read": revenue_read,
        "energy_read": energy_read,
        "activity_read": activity_read,
        "orders_today": orders,
        "revenue_today": revenue,
        "profit_today": profit,
        "roi_percent": roi_percent,
        "recommendation": recommendation
    }
