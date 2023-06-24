from alpaca.trading.client import TradingClient
from alpaca.data import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.requests import CryptoLatestQuoteRequest, StockLatestQuoteRequest, StockBarsRequest, CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical.stock import StockHistoricalDataClient
from gym.envs.env import env
from datetime import datetime

trading_client = TradingClient(env.KEY, env.SECRET, paper=True)
stock_client = StockHistoricalDataClient(env.KEY, env.SECRET)
crypto_client = CryptoHistoricalDataClient(env.KEY, env.SECRET, url_override="")

def get_account():
    return trading_client.get_account()

class Instrument(object):
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
    def get(self):
        pass
    def collection(self, start: datetime, end: datetime):
        pass

class Symbol(Instrument):
    def get(self):
        request = StockLatestQuoteRequest(symbol_or_symbols=self.symbol)
        return stock_client.get_stock_latest_bar(request)
    def collection(self, start: datetime, end: datetime):
        request = StockBarsRequest(
            symbol_or_symbols=self.symbol,
            timeframe=TimeFrame.Minute,
            start=start,
            end=end
        )
        stock_client._use_raw_data = True
        return stock_client.get_stock_bars(request)

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