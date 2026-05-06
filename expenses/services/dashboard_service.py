from ..dal import DataAccessLayer
from collections import defaultdict

class DashboardService:

    def __init__(self):
        self.dal = DataAccessLayer()

    def generate_report(self):
        expenses = self.dal.get_all_expenses()

        data = defaultdict(float)
        total = 0

        for e in expenses:
            data[e.category] += e.amount
            total += e.amount

        percentages = {
            k: (v / total) * 100 if total > 0 else 0
            for k, v in data.items()
        }

        return {
            "totals": dict(data),
            "percentages": percentages
        }