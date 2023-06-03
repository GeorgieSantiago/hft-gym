from enum import Enum
from gymnasium import Env, spaces
import numpy as np
from gyms.envs.models.balance import Balance
from gyms.envs.models.quote import Quote
from gyms.envs.models.position import Position
import gyms.envs.api as api

symbols = [
    "TSLA",
    "GE"
]

quotes: dict = dict()
for symbol in symbols:
    quotes[symbol] = api.get_quotes(list([symbol]))

max_steps = len(quotes[symbols[0]])
class PurchaseAction(Enum):
    SELL = -1
    HOLD = 0
    BUY = 1

class Engine(Env):
    mock: bool = True
    current_step: int = 0
    balance: Balance
    prev_balance: Balance
    positions: list[Position]
    metadata = {'render.modes': ['human']}
    def __init__(self):
        super(Engine, self).__init__()
        low_actions = []
        high_actions = []
        for _ in symbols:
            low_actions.append([-1, 1])
            high_actions.append([1, 100])
        self.action_space = spaces.Box(low=np.array(low_actions), high=np.array(high_actions), shape=(len(symbols), 2), dtype=np.int32)
        self.observation_space = spaces.Box(low=0, high=999, shape=(6, 1))
        self.reset()

    def step(self, actions):
        obs = self._get_obs()
        #print(obs)
        #exit(1)
        self.prev_balance = self.balance
        idx = 0
        for action, percentage in actions:
            self._place_orders(symbols[idx], action, percentage)
            idx += 1
        reward = self._calculate_reward()
        terminate = self.balance.accountValue <= 0
        truncate = len(quotes) == self.current_step
        return obs, reward, terminate, truncate, {}
    def render(self) -> None:
        pass
    def reset(self) -> None:
        self.current_step = 0
        self.balance = self._get_default_balance()
        self.prev_balance = self._get_default_balance()
        self.positions = list()
        return self._get_obs()
    def _place_orders(self, symbol: str, action: int, amount: int) -> None:
        pass
    def _get_order_action(self, value: int) -> PurchaseAction:
        return PurchaseAction(value)
    def _get_obs(self) -> dict:
        _step_quotes = [quotes[symbol][self.current_step % max_steps].to_array(['lastPrice']) for symbol in symbols]
        obs = np.array(_step_quotes)
        self.current_step += 1
        return obs
    def _calculate_reward(self) -> int:
        return self.prev_balance.accountValue - self.balance.accountValue
    def _get_default_balance(self) -> Balance:
        return Balance({
            'accountValue': 100
        })