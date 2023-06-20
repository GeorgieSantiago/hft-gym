from enum import Enum
from gymnasium import Env, spaces
import numpy as np
from gym.envs.models.balance import Balance
from gym.envs.models.quote import Quote
from gym.envs.models.positions import Positions
import gym.envs.api as api

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
    last_action: list = list()
    balance: Balance
    prev_balance: Balance
    positions: Positions
    metadata = {'render_modes': ['human']}
    def __init__(self, live: bool = False):
        super(Engine, self).__init__()
        self.live = live
        low_actions = []
        high_actions = []
        for _ in symbols:
            low_actions.append([-1, 1])
            high_actions.append([1, 100])
        self.action_space = spaces.Box(low=np.array(low_actions), high=np.array(high_actions), shape=(len(symbols), 2), dtype=np.int32)
        self.observation_space = spaces.MultiDiscrete(np.array([[99999] for _ in symbols]))
        #self.observation_space = spaces.Box(low=0, high=999, shape=(len(symbols), 1))
        self.reset()

    def step(self, actions):
        obs = self._get_obs()
        #print(obs)
        #exit(1)
        self.prev_balance = self.balance
        idx = 0
        for action, percentage in actions:
            self._place_orders(idx, action, percentage)
            idx += 1
        reward = self._calculate_reward()
        terminate = self.balance.accountValue <= 0
        truncate = (max_steps - 1) == self.current_step
        return obs, reward, terminate, truncate, {}
    def render(self) -> None:
        print(f"Current Step: {self.current_step}")
    def reset(self, seed = None, options: dict = None) -> tuple((any, dict)):
        self.current_step = 0
        self.balance = self._get_default_balance()
        self.prev_balance = self._get_default_balance()
        self.positions = Positions(symbols)
        print("ENV RESET>>>>>>>>>>")
        return (self._get_obs(), {})
    def _place_orders(self, symbol_idx: str, action: int, amount: int) -> None:
        quote = quotes[symbols[symbol_idx]][self.current_step]
        print(f"Action {action}")
        print(f"Balance ${self.balance.stockBuyingPower}")
        if action == 1:
            max_purchase_amount = int((self.balance.stockBuyingPower / quote.lastPrice))
            purchase_amount = amount
            if max_purchase_amount < amount:
                purchase_amount = int(max_purchase_amount * (amount / 100))
            if purchase_amount > 0:
                cost = purchase_amount * quote.lastPrice
                print(f"Buying {purchase_amount} of {symbols[symbol_idx]} for -${cost}")
                self.balance.change(cost * -1)
                self.positions.insert_or_change(symbols[symbol_idx], purchase_amount)
        if action == -1:
            to_sell = int(self.positions.get_qty(symbols[symbol_idx]) * (amount / 100))
            if to_sell > 0:
                price = quotes[symbols[symbol_idx]].lastPrice * to_sell
                print(f"Selling {to_sell} of {symbols[symbol_idx]} for +${price}")
                self.balance.change(price)
                self.positions.insert_or_change(symbols[symbol_idx], to_sell * -1)
        if action == 0:
            pass
    def _get_order_action(self, value: int) -> PurchaseAction:
        return PurchaseAction(value)
    def _get_obs(self):
        _step_quotes = [quotes[symbol][self.current_step % max_steps].to_array(['lastPrice']) for symbol in symbols]
        self.current_step += 1
        return np.array(_step_quotes)
    def _calculate_reward(self) -> int:
        return self.prev_balance.accountValue - self.balance.accountValue
    def _get_default_balance(self) -> Balance:
        return Balance({
            'accountValue': 100,
            'stockBuyingPower': 200
        })