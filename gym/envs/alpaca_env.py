from typing import Any, SupportsFloat
from gym.envs.financial_env import FinancialEnv
from gym.envs.client import Instrument, Symbol, get_account
import gymnasium.spaces as spaces
import numpy as np


class Alpaca(FinancialEnv):
    def __init__(self) -> None:
        '''TODO make the bounds of the buy action '''
        max_value = 100000
        self.observation_space = spaces.Box(0, 20000, (60, 5))
        self.action_space = spaces.Box(low=np.array([10, 0, 0]), high=np.array([1000, 10, 9]), shape=(3,))

    def step(self, action: Any) -> tuple[Any, SupportsFloat, bool, bool, dict[str, Any]]:
        super().step(action)
        self._order(action)
        obs = self._get_obs()
        reward = self._get_reward(action)
        terminal, truncated = self._get_terminal()
        return obs, reward, terminal, truncated, {}

    def reset(self, *, seed: int | None = None, options: dict[str, Any] | None = None) -> tuple[Any, dict[str, Any]]:
        # super().reset(seed, options)
        self.orders = []
        self.account = self.original_account_state
        self.starting_value = float(self.account.portfolio_value)
        if self.original_start_dt is not None:
            self._reset_simulated_time_steps(self.original_start_dt, self.end_dt, self.interval)
        return self._get_obs(), {}

    def close(self):
        current_account = get_account()
        print(f"Starting balance: {self.starting_value} Ending balance: {current_account.portfolio_value}")
        pass
