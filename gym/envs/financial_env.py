from typing import Any, SupportsFloat
from gymnasium import Env
from gym.envs.client import Instrument, Symbol, get_account, get_open_positions
from datetime import datetime, timedelta

from utils import plot_bars

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
class FinancialEnv(Env):
    def reset(self, *, seed: int | None = None, options: dict[str, Any] | None = None) -> tuple[Any, dict[str, Any]]:
        # super().reset(seed, options)
        self.account = get_account()
        self.starting_value = self.account.portfolio_value
        return (self._get_obs(), {})
    '''
    Virtual methods
    '''
    def step(self, action: Any) -> tuple[Any, SupportsFloat, bool, bool, dict[str, Any]]:
        self.account = get_account()
        pass
    def render(self):
        pass
    def close(self):
        current_account = get_account()
        print(f"Starting balance: {self.starting_value} Ending balance: {current_account.portfolio_value}")
        pass

    '''
    Private Methods
    '''
    def _get_obs(self):
        collection = self.instrument.collection(self.start_dt, self.current_dt)[self.symbol]
        self.current_collection = collection
        obs = plot_bars(collection, self.start_dt, self.current_dt, as_np_array=True)
        self._step_times()
        return obs

    def _step_times(self):
        if self.live:
            self.current_dt = datetime.now()
            self.start_dt = self.current_dt - timedelta(hours=self.interval)
        else:
            next_delta_time = datetime.now()
            delta = self.delta_dt - next_delta_time
            self.delta_dt = next_delta_time
            self.current_dt += delta
            self.start_dt = self.current_dt - timedelta(hours=self.interval)
        if self.debug:
            print("Time step")
            print(self.current_dt, "Current DT")
            print(self.start_dt, "Start DT")
            if self.live == False:
                print(self.delta_dt, "Delta DT")
                print(self.current_dt, "Current DT")

    '''
    Calculate reward of actions
    @TODO Calculate the reward
    Rewards are calculated on a delayed gratification
    By mapping through the orders that are complete but
    not calculated we can derive values from
    1. time * -1 for buy fill time
    2. time * -1 for sell fill time
    3. profit for completed sell orders
    4. loss for stop orders
    '''
    def _get_reward(self, action):
        print("Get reward debug")
        print(action)
        # print(self.data)
        exit(1)
    
    '''
    @TODO Work on correcting the order information
    '''
    def _order(self, action) -> bool:
        if self.debug:
            print(action, "Order called")
        if self._is_action_valid(action):
            buy_price, sell_change, stop_change = action
            self.instrument.order(buy_price, buy_price + sell_change, buy_price - stop_change)
    
    '''
    @TODO check if we are at a terminal state (Past end_dt, account is empty)
    @TODO check if we are at a truncated state
    '''
    def _get_terminal(self) -> tuple((bool, bool)):
        if self.debug:
            print(f"Account cash: {self.account.cash}")
        return tuple(self.account.cash == 0, self.current_dt > self.end_dt and self.live == False)

    '''
    @TODO check against account to see if the action is
    doable
    @TODO check against current orders and limit concurrency
    '''
    def _is_action_valid(self, action) -> bool:
        print(self.account.buying_power, "Buying Power")
        if action[0] > float(self.account.buying_power):
            return False
        orders = get_open_positions(self.symbol)
        print(orders, "Open Orders")
        if len(orders) > 2:
            return False
        
        return True

    def setup(self, symbol: str, interval: int, end_time: datetime = None, start_time: datetime = None, live: bool = False, debug: bool = False):
        self.instrument = Symbol('TSLA')
        self.live = live
        self.debug = debug
        self.symbol = symbol
        self.interval = interval
        self.account = get_account()
        if live == True:
            self.current_dt = datetime.now()
            self.start_dt = self.current_dt - timedelta(hours=interval)
        else:
            self.end_dt = end_time
            self.start_dt = start_time
            self.current_dt = self.start_dt + timedelta(hours=interval)
            self.delta_dt = datetime.now()
        if self.live == False:
            self.data = self.instrument.collection(self.start_dt, self.end_dt)
        if self.debug:
            print(self.instrument)
            #print(self.data)