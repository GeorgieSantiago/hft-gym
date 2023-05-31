import position

class Account(object):
    def __init__(self, id: int, balance: float, positions: list[position.Position]):
        self.id = id
        self.balance = balance
        self.available_funds
        self.positions = positions