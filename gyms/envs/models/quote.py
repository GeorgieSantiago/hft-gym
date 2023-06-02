from models.model import Model

BaseQuote = type('BaseQuote', (Model,), {
        'symbol': None,
        'description': None,
        'bidPrice': None,
        'bidSize': None,
        'bidId': None,
        'askPrice': None,
        'askSize': None,
        'askId': None,
        'lastPrice': None,
        'lastSize': None,
        'lastId': None,
        'openPrice': None,
        'highPrice': None,
        'lowPrice': None,
        'closePrice': None,
        'netChange': None,
        'totalVolume': None,
        'quoteTimeInLong': None,
        'tradeTimeInLong': None,
        'mark': None,
        'exchange': None,
        'exchangeName': None,
        'marginable': None,
        'shortable': None,
        'volatility': None,
        'digits': None,
        '52WkHigh': None,
        '52WkLow': None,
        'peRatio': None,
        'divAmount': None,
        'divYield': None,
        'securityStatus': None,
        'regularMarketLastPrice': None,
        'regularMarketLastSize': None,
        'regularMarketNetChange': None,
        'regularMarketTradeTimeInLong': None
})

class Quote(BaseQuote):
    def __init__(self, json: dict) -> None:
        super().__init__(json)