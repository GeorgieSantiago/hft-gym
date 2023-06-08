from gym.envs.models import Position

class Positions(object):
    _positions: dict = dict()
    def __init__(self, symbols: list[str]):
        for symbol in symbols:
            self._positions[symbol] = 0
    def insert_or_change(self, symbol: str, qty: int) -> None:
        change = self._positions[symbol] + qty if symbol in self._positions.keys() else qty
        self._positions[symbol] = change
    def get_qty(self, symbol: str) -> int:
        return self._positions[symbol]

