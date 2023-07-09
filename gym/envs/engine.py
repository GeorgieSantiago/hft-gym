from gymnasium import Env, spaces
import numpy as np
from alpaca.trading.models import TradeAccount
from gym.envs.client import get_account
from gym.envs.client import Symbol
from utils import plot_bars
from datetime import datetime, timedelta

'''
@TODO main updates

Training:
A start and end time are selected as well as an interval used
to calculate the env obs data. On reset the current date is
calculated by the start date + interval. At each step the delta time
will be added to the current datetime. The start time will then be
calculated as the end time - interval. This will simulate actual
time movement as seen in the live env.

Calculating the reward:
On reset the env will gather the entire data via the start and end
range. This will be used to "look ahead" in the data to calculate the
value of an order.

Live:
Instead only the interval will be selected. The end time will be
calculated as now and the start time will be end_time - interval
(done artificially in the training step via the delta time)

This window will be used to request the bars of a specified
instrument and that response will be converted in to image and then 
an np.array for use by the agent

'''

class Engine(Env):
    account: TradeAccount
    metadata = {'render_modes': ['human']}
    def __init__(self, symbol: str = "TSLA", live: bool = False):
        super(Engine, self).__init__()
        self.step_counter = 0
        self.symbol = symbol
        self.live = live
        obs_shape = self._setup()
        self.observation_space = spaces.Box(low=0, high=255, shape=obs_shape)
        self.action_space = spaces.Box(low=0, high=1000, shape=(3,))
        self.reset()
    
    def step(self, actions):
        self._handle_action(actions)
        obs = self._get_obs()
        reward = self._get_reward()
        terminate, truncate = self._is_terminal()
        return obs, reward, terminate, truncate, {}
    
    def render(self) -> None:
        print(f"Current Step: {self.current_step}")

    def reset(self, seed = None, options: dict = None) -> tuple((any, dict)):
        #TODO redo reset method
        self.account = get_account()
        return (self._get_obs(), {})
    
    '''
    @TODO convert this to a request
    '''
    def _get_obs(self):
        if not self.live:
            obs = self.images[self.step_counter]
            self.step_counter += 1
            return obs

    '''
    @TODO Calculate the reward
    Rewards are calculated on a delayed gratification
    By mapping through the orders that are complete but
    not calculated we can derive values from
    1. time * -1 for buy fill time
    2. time * -1 for sell fill time
    3. profit for completed sell orders
    4. loss for stop orders
    '''
    def _get_reward(self, action) -> int:
        return 0
    
    '''
    @TODO place order
    If the action is valid (useing _is_valid_action)
    then execute the order [Limit buy] -> OTO (OCO( Sell, Stop loss ))
    '''
    def _handle_action(self, action) -> None:
        if self.live:
            #@NOTE Highway to the danger zone!
            buy_price, sell_price, stop_price = action
            if self._is_valid_action(action):
                self.instrument.order(buy_price, sell_price, stop_price)
        

    '''
    @TODO figure out of the state is terminal (Account is empty)
    @TODO figure out if we are out of datasets
    @TODO figure out if we can reset the paper account dynamically
    '''
    def _is_terminal(self) -> tuple(bool,bool):
        return self.account.cash < 50000
    
    '''
    @TODO figure out if the action is valid based on the difference
    between the account buying power - action buy price (action[0])
    '''
    def _is_valid_action(self, action) -> bool:
        return True
    
    '''
    @TODO Check if any active orders have closed in this timestep
    These funds should be added back into the account at the expected
    limit sell price and mark the order as closed
    '''
    def _handle_order_close(self):
        pass
    
    '''
    @TODO Check if any active orders haved stopped. return the funds at the 
    stop price * qty and set the order to complete
    '''
    def _handle_order_stop(self):
        pass
    '''          
    @TODO depreca for real time or timeseries based observations
    '''
    def _setup(self):
        print("Building env data...")
        self.instrument = Symbol('TSLA')
        self.data = list()
        backward_steps = 100
        obs_shape = None
        for i in range(backward_steps):
            start_dt = datetime.today() - timedelta(1) - timedelta(i)
            end_dt = datetime.today() - timedelta(i)
            stock_day_data = self.instrument.collection(start_dt, end_dt)
            # print(stock_day_data)
            self.data.append(stock_day_data)
        symbol_data = self.data[0]['TSLA']
        self.images = list()
        for i in range(len(symbol_data)):
            batch = symbol_data[:i]
            if len(batch) == 0:
                continue
            start_dt = datetime.fromisoformat(batch[0]['t'])
            end_dt = datetime.fromisoformat(batch[-1]['t'])
            img = plot_bars(batch, start_dt, end_dt, as_np_array=True)
            if obs_shape == None:
                obs_shape = img.shape
            self.images.append(img)
        
        print(f"Env has {len(self.images)} data frames")
        return obs_shape