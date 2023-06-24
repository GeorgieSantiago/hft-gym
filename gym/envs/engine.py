from gymnasium import Env, spaces
import numpy as np
from gym.envs.client import get_account
from utils import plot_bars

class Engine(Env):
    metadata = {'render_modes': ['human']}
    def __init__(self, live: bool = False):
        super(Engine, self).__init__()
        self.live = live
        low_actions = []
        high_actions = []
        #TODO new action spaces and obs spaces
        #self.observation_space = spaces.Box(low=0, high=999, shape=(len(symbols), 1))
        self.reset()

    def step(self, actions):
        obs = self._get_obs()
        #TODO redo step function
        return obs, reward, terminate, truncate, {}
    def render(self) -> None:
        print(f"Current Step: {self.current_step}")
    def reset(self, seed = None, options: dict = None) -> tuple((any, dict)):
        #TODO redo reset method
        self.account = get_account()
        print("ENV RESET>>>>>>>>>>")
        return (self._get_obs(), {})
    def _place_orders(self, buy_price, sell_price) -> None:
        #TODO hook this up to the API
        pass