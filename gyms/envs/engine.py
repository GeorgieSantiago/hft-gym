from gymnasium import gym, spaces
import numpy as np

'''
    Action Space:
    for each symbol
    [
        [buy|sell|nothing] = -1 0 1 (sign of the first value)
        [percentage] = 1 - 100
    ]
    if buy get total amount possible to buy and place an order
    to buy a % of that

    if sell get the total amount held and place an order to sell
    the % of that

    Example action output
    [[ 1 83]
    [-1 67]
    [ 1 58]]


    observation space
    This uses the HOLC shape for each symbol

    example observation space
    [[729.42896  640.5956   196.64128  465.47382 ]
    [806.8653   191.71783  981.9553   578.2849  ]
    [513.8814   123.039116 548.7596   437.76187 ]
    [918.3371   657.2043   490.68494  721.82446 ]
    [298.56995  636.23193  377.30753  650.08466 ]]


'''

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
        self.action_space = spaces.Box(low=np.array(low_actions), high=np.array(high_actions), shape=(len(symbols), 2), dtype=np.int32)
        self.observation_space = spaces.Box(low=0, high=999, shape=(6, 4))
    '''
      @params actions [buy|sell|nothing, percentage]
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
