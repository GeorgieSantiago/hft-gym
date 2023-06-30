from alpaca.trading.client import TradingClient
from alpaca.data import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.requests import CryptoLatestQuoteRequest, StockLatestQuoteRequest, StockBarsRequest, CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.requests import LimitOrderRequest, TakeProfitRequest, StopLossRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderClass
from alpaca.trading.models import TradeAccount
from alpaca.data.historical.stock import StockHistoricalDataClient
from gym.envs.env import env
from datetime import datetime
from decimal import Decimal

trading_client = TradingClient(env.KEY, env.SECRET, paper=True)
stock_client = StockHistoricalDataClient(env.KEY, env.SECRET)
crypto_client = CryptoHistoricalDataClient(env.KEY, env.SECRET, url_override="")

def get_account() -> TradeAccount:
    account: TradeAccount = trading_client.get_account()
    return account

def get_all_assets():
    return trading_client.get_all_assets()

def get_orders():
    return trading_client.get_orders()

def get_open_positions(symbol: str):
    return trading_client.get_all_positions()
    try:
        return trading_client.get_open_position(symbol_or_asset_id=symbol)
    except:
        return []

class Instrument(object):
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
    def get(self):
        pass
    def collection(self, start: datetime, end: datetime):
        pass
    def order(self, buy_price: float, sell_price: float, stop_price: float) -> None:
        pass

class Symbol(Instrument):
    def get(self):
        request = StockLatestQuoteRequest(symbol_or_symbols=self.symbol)
        return stock_client.get_stock_latest_quote(request)
        # return stock_client.get_stock_latest_bar(request)
    def collection(self, start: datetime, end: datetime):
        request = StockBarsRequest(
            symbol_or_symbols=self.symbol,
            timeframe=TimeFrame.Minute,
            start=start,
            end=end
        )
        stock_client._use_raw_data = True
        return stock_client.get_stock_bars(request)
    '''
    @TODO Values are long floats and need to be double
    this is broken right now

    Need to make the action formula conform to the rules
    of the request. This should be a lot easier with the
    limit buy in place.
    '''
    def order(self, buy_price: float, sell_price: float, stop_price: float) -> None:
        buy_price = round(buy_price, 2)
        sell_price = round(sell_price, 2)
        stop_price = round(stop_price, 2)
        print(buy_price, sell_price, stop_price)
        take_profit = TakeProfitRequest(
            limit_price=sell_price,
        )

        stop_loss = StopLossRequest(
            limit_price=stop_price,
            stop_price=stop_price
        )

        request = LimitOrderRequest(
            symbol=self.symbol,
            qty=2,
            limit_price=buy_price,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY,
            order_class=OrderClass.BRACKET,
            take_profit=take_profit,
            stop_loss=stop_loss,
        )
        trading_client._use_raw_data = True
        trading_client.submit_order(request)


class Crypto(Instrument):
    def get(self):
        request = CryptoLatestQuoteRequest(symbol_or_symbols=self.symbol)
        return crypto_client.get_crypto_latest_bar(request)
    def collection(self, start: datetime, end: datetime):
        request = CryptoBarsRequest(
            symbol_or_symbols=self.symbol,
            timeframe=TimeFrame.Minute,
            start=start,
            end=end
        )
        return crypto_client.get_crypto_bars(request)