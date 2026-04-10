from datetime import datetime

class ARCROIEngine:
    def __init__(self):
        self.revenue_events = []
        self.guest_count = 0
        self.interventions = []

    def log_revenue(self, amount):
        self.revenue_events.append({
            "amount": amount,
            "timestamp": datetime.now()
        })

    def log_guest(self, count=1):
        self.guest_count += count

    def log_intervention(self, name):
        self.interventions.append({
            "name": name,
            "timestamp": datetime.now()
        })

    def total_revenue(self):
        return round(sum(event["amount"] for event in self.revenue_events), 2)

    def revenue_per_guest(self):
        if self.guest_count == 0:
            return 0
        return round(self.total_revenue() / self.guest_count, 2)

    def revenue_per_hour(self):
        if not self.revenue_events:
            return 0

        start = self.revenue_events[0]["timestamp"]
        end = self.revenue_events[-1]["timestamp"]
        hours = max((end - start).total_seconds() / 3600, 1)
        return round(self.total_revenue() / hours, 2)

    def roi_report(self):
        return {
            "total_revenue": self.total_revenue(),
            "guest_count": self.guest_count,
            "revenue_per_guest": self.revenue_per_guest(),
            "revenue_per_hour": self.revenue_per_hour(),
            "interventions": len(self.interventions),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
