from typing import Any, SupportsFloat
from uuid import uuid4, UUID
from gymnasium import Env
from gym.envs.client import Symbol, Instrument, get_account, get_open_positions
from datetime import datetime, timedelta
from gym.envs.mock_order import MockOrder, create_order
from gym.envs.report_card import ReportCard
from utils import plot_bars
from alpaca.trading.models import TradeAccount, Position, Order
from alpaca.trading.enums import OrderStatus
from gym.envs.models.tick import Tick


def collection(data: list):
    return [Tick(d).to_array() for d in data]


class FinancialEnv(Env):
    consecutive_closed_orders: int = 0
    live: bool = False
    debug: bool = False
    positions: list[Position]
    orders: list[Order | MockOrder]
    account: TradeAccount
    data: dict
    symbol: str
    interval: int
    starting_value: float
    instrument: Instrument
    current_dt: datetime
    start_dt: datetime
    original_start_dt: datetime
    tzinfo: datetime.tzinfo

    def step(self, action):
        if self.live:
            self.account = get_account()
        self._order_step()
        self._step_times()
        pass

    def _get_obs(self):
        data = self.instrument.collection(self.start_dt, self.current_dt)[self.symbol] \
            if self.live else self._get_time_step_collection(self.start_dt, self.current_dt)
        self.current_collection = data
        return collection(data)
        # obs = plot_bars(collection, self.start_dt, self.current_dt, as_np_array=True)
        # return obs

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

    def _get_reward(self, action):
        buy_price, sell_price, stop_price = self._get_action(action)
        # @NOTE the actual order timestamp is slightly diff from this one
        order = create_order(buy_price, sell_price, stop_price, self.tzinfo)
        future_values = self._get_time_step_collection(self.current_dt, self.end_dt)
        report_card = ReportCard()
        is_open: bool = False
        close_time: timedelta
        for i in range(len(future_values)):
            value = future_values[i]
            open_price = float(value['o'])
            close_price = float(value['c'])
            high = max(open_price, close_price)
            low = min(open_price, close_price)

            ts = self._ts(value['t'])
            if is_open:
                if low <= order.close_price <= high:
                    self.consecutive_closed_orders += 1
                    diff: timedelta = ts - order.created_at
                    profit = order.close_price - order.open_price
                    report_card \
                        .status(OrderStatus.FILLED) \
                        .fill_time(diff.total_seconds() + (abs(close_time.total_seconds()))) \
                        .profit(profit) \
                        .change(self.consecutive_closed_orders)
                    break
                if low <= order.stop_price <= high:
                    self.consecutive_closed_orders = 0
                    diff: timedelta = ts - order.created_at
                    loss = order.stop_price - order.open_price
                    report_card \
                        .status(OrderStatus.STOPPED) \
                        .profit(loss) \
                        .fill_time(diff.total_seconds() + (abs(close_time.total_seconds())))
                    break
                continue
            else:
                if low <= order.open_price <= high:
                    is_open = True
                    diff: timedelta = ts - order.created_at
                    close_time = diff
                    report_card.fill_time(int(diff.total_seconds()))
        if not is_open:
            report_card.change(-25)
        return report_card()

    def _order(self, action) -> bool:
        if self._is_action_valid(action):
            buy_price, sell_price, stop_price = self._get_action(action)
            if self.live:
                # TODO Work on correcting the order information
                self.instrument.order(buy_price, sell_price, stop_price)
                return True
            else:
                cost = buy_price * 2
                self._update_account(cost * -1)
                order = create_order(buy_price, sell_price, stop_price, self.tzinfo)
                self.orders.append(order)
                return True
        return False

    def _get_terminal(self) -> tuple[bool, bool]:
        return self.account.cash == 0, self.current_dt > self.end_dt is not None and not self.live

    def _is_action_valid(self, action) -> bool:
        if action[0] > float(self.account.buying_power):
            return False
        orders = get_open_positions(self.symbol) if self.live else self._get_orders_by_status(OrderStatus.ACCEPTED)
        if len(orders) > 2:
            return False
        return True

    def setup(self, symbol: str, interval: int, end_time: datetime = None, start_time: datetime = None,
              live: bool = False, debug: bool = False):
        self.orders = []
        self.data = {}
        self.instrument = Symbol('TSLA')
        self.live = live
        self.debug = debug
        self.symbol = symbol
        self.interval = interval
        self.account = get_account()
        self.original_account_state = self.account
        data = self.instrument.collection(start_time, end_time)
        for entry in data[self.symbol]:
            self.data[entry['t']] = entry
        t = list(self.data.keys())[0][:-1] # remove the 'Z' from the iso string
        self.tzinfo = datetime.fromisoformat(t).tzinfo
        if live:
            self.current_dt = datetime.now()
            self.start_dt = self.current_dt - timedelta(hours=interval)
        else:
            self.original_start_dt = start_time.replace(tzinfo=self.tzinfo)
            self._reset_simulated_time_steps(start_time, end_time, interval)

    def _reset_simulated_time_steps(self, start_time, end_time, interval):
        self.end_dt = end_time.replace(tzinfo=self.tzinfo)
        self.start_dt = start_time.replace(tzinfo=self.tzinfo)
        self.current_dt = self.start_dt + timedelta(hours=interval)
        self.delta_dt = datetime.now(self.tzinfo)
        self._step_times()

    def _get_orders_by_status(self, status: OrderStatus):
        return [order for order in self.orders if order.status == status]

    def _get_time_step_collection(self, start_dt: datetime, end_dt: datetime) -> list:
        keys = [t for t in self.data.keys() if start_dt < self._ts(t) < end_dt]
        return [self.data[key] for key in keys]

    def _order_step(self):
        #todo double check this
        current = self._get_time_step_collection(self.start_dt, self.current_dt)[-1]
        open_orders = self._get_orders_by_status(OrderStatus.ACCEPTED)
        pending_orders = self._get_orders_by_status(OrderStatus.PENDING_NEW)
        high = max((float(current['c']), float(current['o'])))
        low = min((float(current['c']), float(current['o'])))
        closed_orders = [order.id for order in open_orders if
                         low <= order.close_price <= high]
        stopped_orders = [order.id for order in open_orders if
                          low <= order.stop_price <= high]
        opened_orders = [order.id for order in pending_orders if
                         low <= order.open_price <= high]
        self._update_orders(opened_orders, status=OrderStatus.ACCEPTED)
        self._update_orders(closed_orders, status=OrderStatus.FILLED)
        self._update_orders(stopped_orders, status=OrderStatus.STOPPED)

    def _update_orders(self, ids: list[UUID], status: OrderStatus):
        for idx in range(len(self.orders)):
            if self.orders[idx].id in ids:
                order = self.orders[idx]
                print(f"Order {idx} updating to status:{status}")
                print(f"open {order.open_price} close {order.close_price} stop {order.stop_price}")
                self.orders[idx].status = status
                liquid_value = self.orders[idx].close_price if status == OrderStatus.FILLED else self.orders[
                    idx].stop_price
                self._update_account(liquid_value)

    def _update_account(self, total: float):
        shared = total / 2
        self.account.buying_power = float(self.account.buying_power) + total
        self.account.regt_buying_power = float(self.account.regt_buying_power) + total
        self.account.non_marginable_buying_power = float(self.account.non_marginable_buying_power) + shared
        self.account.cash = float(self.account.cash) + shared

    def _find_by_price(self, price: float):
        prices = self._get_time_step_collection(self.current_dt, self.end_dt)
        print(prices)
        exit(1)

    def _ts(self, timestamp: str) -> datetime:
        return datetime.fromisoformat(timestamp[:-1]).replace(tzinfo=self.tzinfo)

    def _get_action(self, action):
        buy_price, sell_change, stop_change = action
        return buy_price, buy_price + sell_change, buy_price - stop_change
