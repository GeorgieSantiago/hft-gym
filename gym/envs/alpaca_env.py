from typing import Any, SupportsFloat
from gym.envs.financial_env import FinancialEnv
from gym.envs.client import Instrument, Symbol
from gymnasium.spaces import Box
import numpy as np

class Alpaca(FinancialEnv):
    def __init__(self) -> None:
        '''TODO make the bounds of the buy action '''
        self.observation_space = Box(low=0, high=255, shape=(575, 800, 4))
        self.action_space = Box(low=np.array([10, 0, 0]), high=np.array([1000, 10, 9]), shape=(3,))
    def step(self, action: Any) -> tuple[Any, SupportsFloat, bool, bool, dict[str, Any]]:
        super().step(action)
        self._order(action)
        obs = self._get_obs()
        reward = self._get_reward(action)
        terminal, truncated = self._get_terminal()
        return obs, reward, terminal, truncated, {}
    
    '''
    @TODO
    '''
    def render(self):
        pass