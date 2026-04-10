import time

revenue_events = []


def log_revenue_event(moment_name, revenue_before, revenue_after):
    impact = revenue_after - revenue_before

    event = {
        "timestamp": time.time(),
        "moment": moment_name,
        "revenue_before": revenue_before,
        "revenue_after": revenue_after,
        "impact": impact
    }

    revenue_events.append(event)

    return event


def get_revenue_summary():
    if not revenue_events:
        return {"status": "no data"}

    total_impact = sum(e["impact"] for e in revenue_events)

    return {
        "events_logged": len(revenue_events),
        "total_revenue_impact": total_impact,
        "events": revenue_events[-10:]
    }
