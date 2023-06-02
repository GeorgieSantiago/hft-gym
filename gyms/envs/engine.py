from gymnasium import gym, spaces
import numpy as np
from models.account import Account, Price
import api

symbols = [
    "TSLA",
    "APPL",
    "GE"
]

class Engine(gym.Env):
    prices: list[Price]
    account: Account
    metadata = {'render.modes': ['human']}
    def __init__(self):
        super(Engine, self).__init__()
        low_actions = []
        high_actions = []
        for _ in symbols:
            low_actions.append([-1, 1])
            high_actions.append([1, 100])
        self.action_space = spaces.Box(low=np.array(low_actions), high=np.array(high_actions), shape=(len(symbols), 2), dtype=np.int32)
        self.observation_space = spaces.Box(low=0, high=999, shape=(6, 4))
        self.reset()
    '''
      @params actions [buy|sell|nothing, percentage]
      @returns [observation, reward, terminate, info]
    '''
    def step(self, action) -> list[dict, dict, int, bool]:
        pass
    def render(self) -> None:
        pass
    def _get_obs(self) -> dict:
        pass
    def reset(self) -> None:
        for symbol in symbols:
            self.prices[symbol] = api.get_price_history(symbol)
        self.account.balance = 1000
        self.account.positions = list()