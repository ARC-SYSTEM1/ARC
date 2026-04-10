from arc_roi_engine import get_roi_metrics
from arc_kpi_engine import get_kpi_metrics
from arc_orders_engine import orders_today
from arc_state import get_state


def get_end_of_day():
    """
    ARC End-of-Day Assessment
    Combines ROI, KPI, state, and transaction tracker
    for final nightly venue evaluation.
    """

    roi = get_roi_metrics()
    kpi = get_kpi_metrics()
    orders = orders_today()
    state = get_state()

    revenue = roi.get("revenue_today", 0)
    profit = roi.get("profit_today", 0)
    roi_percent = roi.get("roi_percent", 0)

    orders_count = orders.get("orders_today", 0)

    activity = kpi.get("activity_score", 0)
    energy = kpi.get("energy_score", 0)

    mode = state.get("mode", "UNKNOWN")

    # Performance evaluation
    if revenue == 0:
        performance = "No revenue recorded"
    elif roi_percent < 0:
        performance = "Revenue below operating cost"
    elif roi_percent < 40:
        performance = "Low profitability"
    elif roi_percent < 100:
        performance = "Moderate profitability"
    else:
        performance = "Strong profitability"

    # Energy evaluation
    if energy == 0:
        energy_read = "No activity"
    elif energy < 3:
        energy_read = "Low energy"
    elif energy < 6:
        energy_read = "Moderate energy"
    else:
        energy_read = "High energy"

    return {
        "orders_today": orders_count,
        "revenue_today": revenue,
        "profit_today": profit,
        "roi_percent": roi_percent,
        "activity_score": activity,
        "energy_score": energy,
        "mode": mode,
        "performance_summary": performance,
        "energy_summary": energy_read
    }

