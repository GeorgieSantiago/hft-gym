from gymnasium import spaces
import numpy as np

tickers = [
    'APPL',
    'FUV',
    'TSLA'
]
# Actions of the format Symbol Buy x%, Symbol Sell x%, Symbol Hold, etc.
#action_space = spaces.Box(low=np.array([0, 0, 0], dtype=np.float32), high=np.array([2, 9, 9]))
#action_space = spaces.Discrete(3)
# action_space = spaces.Tuple((
#     spaces.Discrete(3),
#     spaces.Discrete(len(tickers)),
#     spaces.Discrete(101)
# ))
# action_space = spaces.MultiDiscrete(np.array([2, len(tickers), 101]))
low_actions = []
high_actions = []
for ticker in tickers:
    low_actions.append([-1, 1])
    high_actions.append([1, 100])
action_space = spaces.Box(low=np.array(low_actions), high=np.array(high_actions), shape=(len(tickers), 2), dtype=np.int32)
#other_action_space = spaces.Box(low=np.array([-1, 0, 0]), high=np.array([1, len(tickers), 100]), shape=(3,))
# Prices contains the OHCL values for the last five prices
observation_space = spaces.Box(low=0, high=999, shape=(6, 6))
print(observation_space.sample())
print(action_space.sample())
custom_space = spaces.Dict()