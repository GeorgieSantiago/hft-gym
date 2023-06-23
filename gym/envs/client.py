from alpaca.trading.client import TradingClient
from alpaca.data import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.requests import CryptoLatestQuoteRequest, StockLatestQuoteRequest, StockBarsRequest, CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical.stock import StockHistoricalDataClient
from gym.envs.env import env
from datetime import datetime

trading_client = TradingClient(env.KEY, env.SECRET, paper=True)
stock_client = StockHistoricalDataClient(env.KEY, env.SECRET)
stock_historical_client = StockHistoricalDataClient(env.KEY, env.SECRET)
crypto_historical_client = CryptoHistoricalDataClient(env.KEY, env.SECRET)

class Instrument(object):
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
    def get(self):
        pass
    def collection(self, start: datetime, end: datetime):
        request = CryptoBarsRequest(symbol_or_symbols=self.symbol)

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
        return stock_historical_client.get_stock_bars(request).df

class Crypto(Instrument):
    def get(self):
        request = CryptoLatestQuoteRequest(symbol_or_symbols=self.symbol)
        return crypto_historical_client.get_crypto_latest_bar(request)
    def collection(self, start: datetime, end: datetime):
        request = CryptoBarsRequest(
            symbol_or_symbols=self.symbol,
            timeframe=TimeFrame.Minute,
            start=start,
            end=end
        )
        return crypto_historical_client.get_crypto_bars(request).df


def d_test():
    tsla = Symbol("TSLA")
    eth = Crypto("ETH/USD")
    print("Quote:")
    print(tsla.get())
    print("Bars \n")
    print(tsla.collection(datetime(2022, 6, 17), datetime(2022, 6, 19)))