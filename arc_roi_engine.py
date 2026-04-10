from arc_state import get_state
from arc_orders_engine import orders_today, order_stats

def get_roi_metrics():
    state = get_state()
    today = orders_today()
    stats = order_stats()

    presence = 1 if state.get("presence", False) else 0
    activity = int(state.get("activity", 0) or 0)
    energy = int(state.get("energy", 0) or 0)

    revenue_today = float(today.get("revenue_today", 0) or 0)
    orders_count = int(today.get("orders_today", 0) or 0)
    avg_ticket = float(stats.get("average_ticket", 0) or 0)

    estimated_cost = 120 + (activity * 20) + (energy * 15)
    profit_today = revenue_today - estimated_cost

    roi_percent = round((profit_today / estimated_cost) * 100, 1) if estimated_cost > 0 else 0.0

    guests_present = max(1, activity * 4) if presence else 0
    revenue_per_guest = round(revenue_today / guests_present, 1) if guests_present > 0 else 0

    if roi_percent < 40:
        roi_status = "weak"
    elif roi_percent < 100:
        roi_status = "watch"
    else:
        roi_status = "strong"

    return {
        "orders_today": orders_count,
        "revenue_today": revenue_today,
        "average_ticket": avg_ticket,
        "estimated_cost": estimated_cost,
        "profit_today": profit_today,
        "roi_percent": roi_percent,
        "revenue_per_guest": revenue_per_guest,
        "roi_status": roi_status
    }
