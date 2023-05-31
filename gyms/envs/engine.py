from gymnasium import gym, spaces
import numpy as np

symbols = [
    "TSLA",
    "APPL",
    "GE"
]

class Engine(gym.Env):
    metadata = {'render.modes': ['human']}
    def __init__(self):
        super(Engine, self).__init__()
        low_actions = []
        high_actions = []
        for _ in symbols:
            low_actions.append([-1, 1])
            high_actions.append([1, 100])
        '''
        Actions:
        [buy|sell|nothing] = -1 0 1 (sign of the first value)
        [percentage] = 1 - 100
        '''
        self.action_space = spaces.Box(low=np.array(low_actions), high=np.array(high_actions), shape=(len(symbols), 2), dtype=np.int32)
        self.observation_space = spaces.Box(low=0, high=999, shape=(6, 6))
    '''
      @params actions [symbol, buy|sell, price]
      @returns [observation, reward, terminate, info]
    '''
    def step(self, action):
        pass
    def render(self):
        pass
    def _get_obs(self):
        pass
    def reset(self):
        pass
