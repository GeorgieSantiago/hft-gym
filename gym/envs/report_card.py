from math import exp

from alpaca.trading.enums import OrderStatus
from datetime import timedelta

from mpmath import ln
from numpy import arctan


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
            self.score -= 10
        return self
    
    def fill_time(self, timespan: int):
        diff = round((timespan / 60 / 60) * -1) * 0.0001
        self.score += self.g(diff)
        return self

    def g(self, x):
        return 1 - exp(-x)
    
    def profit(self, amount: float):
        self.score += amount
        return self