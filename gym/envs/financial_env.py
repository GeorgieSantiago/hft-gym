from typing import Any, SupportsFloat
from uuid import uuid4, UUID
from gymnasium import Env
from gym.envs.client import Symbol, get_account, get_open_positions
from datetime import datetime, timedelta
from gym.envs.mock_order import MockOrder
from utils import plot_bars
from alpaca.trading.models import TradeAccount, Position, Order
from alpaca.trading.enums import OrderStatus

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


@TODO

Training - Simulate the orders and transactions
- Simulate stopped orders
- Simulate sold orders

Eval - Against paper trading

Production - Against real account

'''

class FinancialEnv(Env):
    account: TradeAccount
    positions: list[Position] = list()
    orders: list[Order | MockOrder] = list()
    data: dict = dict()
    def reset(self, *, seed: int | None = None, options: dict[str, Any] | None = None) -> tuple[Any, dict[str, Any]]:
        # super().reset(seed, options)
        self.account = get_account()
        self.starting_value = self.account.portfolio_value
        if self.original_start_dt != None:
            self._reset_simulated_timesteps(self.original_start_dt, self.end_dt, self.interval)
        return (self._get_obs(), {})
    '''
    Virtual methods
    '''
    def step(self, action: Any) -> tuple[Any, SupportsFloat, bool, bool, dict[str, Any]]:
        if self.live:
            self.account = get_account()
        self._step_times()
        self._close_orders()
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
        collection = self.instrument.collection(self.start_dt, self.current_dt)[self.symbol] \
                        if self.live else self._get_timestep_collection(self.start_dt, self.current_dt)
        self.current_collection = collection
        obs = plot_bars(collection, self.start_dt, self.current_dt, as_np_array=True)
        return obs


    def _step_times(self):
        if self.live:
            self.current_dt = datetime.now(self.tzinfo)
            self.start_dt = self.current_dt - timedelta(minutes=self.interval)
        else:
            next_delta_time = datetime.now(self.tzinfo)
            delta = self.delta_dt - next_delta_time
            self.delta_dt = next_delta_time
            self.current_dt += delta
            self.start_dt = self.current_dt - timedelta(minutes=self.interval)

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
        buy_price, sell_change, stop_change = action
        order = self._create_order(buy_price, buy_price + sell_change, buy_price - stop_change)
        future_values = self._get_timestep_collection(self.current_dt, self.end_dt)
        for i in range(len(future_values)):
            value = future_values[i]
            print(value)
            print(order)
            exit(1) 
        print(future_values)
        # print(self.data)
        exit(1)
    
    '''
    @TODO Work on correcting the order information
    '''
    def _order(self, action) -> bool:
        self.debug_message(action)
        if self._is_action_valid(action):
            buy_price, sell_change, stop_change = action
            if self.live:
                self.instrument.order(buy_price, buy_price + sell_change, buy_price - stop_change)
            else:
                cost = buy_price * 2
                self._update_account(cost * -1)
                order = self._create_order(buy_price, buy_price + sell_change, buy_price - stop_change)
                self.orders.append(order)

    def _get_terminal(self) -> tuple((bool, bool)):
        if self.debug:
            print(f"Account cash: {self.account.cash}")
        return tuple(self.account.cash == 0, self.current_dt > self.end_dt and self.live == False)

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
        self.orders = []
        self.instrument = Symbol('TSLA')
        self.live = live
        self.debug = debug
        self.symbol = symbol
        self.interval = interval
        self.account = get_account()
        data = self.instrument.collection(start_time, end_time)
        for entry in data[self.symbol]:
            self.data[entry['t']] = entry
        t = list(self.data.keys())[0]
        self.tzinfo = datetime.fromisoformat(t).tzinfo
        if live == True:
            self.current_dt = datetime.now()
            self.start_dt = self.current_dt - timedelta(hours=interval)
        else:
            self.original_start_dt = start_time.replace(tzinfo=self.tzinfo)
            self._reset_simulated_timesteps(start_time, end_time, interval)
        self.debug_message("Setup complete!")

    def debug_message(self, msg):
        if self.debug:
            print(msg)

    def _reset_simulated_timesteps(self, start_time, end_time, interval):
        self.end_dt = end_time.replace(tzinfo=self.tzinfo)
        self.start_dt = start_time.replace(tzinfo=self.tzinfo)
        self.current_dt = self.start_dt + timedelta(hours=interval)
        self.delta_dt = datetime.now(self.tzinfo)

    def _get_open_orders(self) -> list[Order | MockOrder]:
        return [order for order in self.orders if order.status == OrderStatus.ACCEPTED]

    def _get_timestep_collection(self, start_dt: datetime, end_dt: datetime) -> list:
        keys = [t for t in self.data.keys() if datetime.fromisoformat(t).replace(tzinfo=self.tzinfo) > start_dt and datetime.fromisoformat(t).replace(tzinfo=self.tzinfo) < end_dt]
        print("Timestep collection count ", len(keys))
        return [self.data[key] for key in keys]
    
    def _create_order(self, open_price, close_price, stop_price) -> MockOrder:
        return MockOrder(
            uuid4(),
            datetime.now(self.tzinfo),
            open_price,
            close_price,
            stop_price,
            OrderStatus.ACCEPTED
        )
    def _close_orders(self):
        current = self._get_timestep_collection(self.start_dt, self.current_dt)[-1]
        open_orders = self._get_open_orders()
        closed_orders = [order.id for order in open_orders if order.close_price <= current['c']]
        stopped_orders = [order.id for order in open_orders if order.stop_price >= current['c']]
        self._update_orders(closed_orders, status=OrderStatus.FILLED)
        self._update_orders(stopped_orders, OrderStatus.STOPPED)

    def _update_orders(self, ids: list[UUID], status: OrderStatus):
        for idx in range(len(self.orders)):
            if self.orders[idx].id in ids:
                self.orders[idx].status = status
                liquid_value = self.orders[idx].close_price if status == OrderStatus.FILLED else self.orders[idx].stop_price
                self._update_account(liquid_value)

    def _update_account(self, total: float):
        shared = total / 2
        self.account.buying_power = float(self.account.buying_power) + total
        self.account.regt_buying_power = float(self.account.regt_buying_power) + total
        self.account.non_marginable_buying_power = float(self.account.non_marginable_buying_power) + shared
        self.account.cash = float(self.account.cash) + shared
    def _find_by_price(self, price: float):
        collection = self._get_timestep_collection(self.current_dt, self.end_dt)
        print(collection)
        exit(1)