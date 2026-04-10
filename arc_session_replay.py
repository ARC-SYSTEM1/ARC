from arc_night_replay import get_night_replay

def get_session_replay():
    replay = get_night_replay()
    raw_events = replay.get("replay", [])

    summary = []
    counts = {}

    for item in raw_events[-40:]:
        event = item.get("event", "unknown")
        value = item.get("value", "unknown")

        label = f"{event}: {value}"
        summary.append(label)

        counts[label] = counts.get(label, 0) + 1

    top_events = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:8]

    return {
        "recent_summary": summary[-15:],
        "top_events": top_events,
        "total_events_reviewed": len(raw_events[-40:])
    }
