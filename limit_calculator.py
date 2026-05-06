class LimitCalculator:

    def calculate_safe_daily_limit(self, total, days):
        if days == 0:
            return 0
        return total / days