from alpaca.trading.enums import OrderStatus
from datetime import timedelta

class ReportCard(object):
    score: int = 0

    def __call__(self, *args, **kwargs):
        return round(self.score)

    def change(self, amount: int):
        self.score += amount
        return self

    def status(self, status: OrderStatus):
        if status == OrderStatus.FILLED:
            self.score += 1
        if status == OrderStatus.STOPPED:
            self.score -= 100
        return self
    
    def fill_time(self, timespan: int):
        self.score += timespan / 60 / 60
        return self
    
    def profit(self, amount: float):
        self.score += amount
        return self
