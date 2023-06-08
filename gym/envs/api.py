import requests
from gym.envs.models.prices import Price
from gym.envs.models.quote import Quote

BASE_URL = "http://127.0.0.1:8000/api"

def get_price_history(symbol: str) -> list[Price]:
    response: requests.Response = requests.get(f"{BASE_URL}/price/history/{symbol}")
    prices = list()
    for data in response.json():
        prices.append(Price(data))
    return prices

def get_quote(symbol: str) -> Quote:
    response: requests.Response = requests.get(f"{BASE_URL}/qoute/{symbol}")
    return Quote(response.json())

def get_quotes(symbols: list[str]) -> list[Quote]:
    quotes = list()
    response = requests.Response = requests.get(f"{BASE_URL}/quotes/search?symbols={','.join(symbols)}")
    for quote in response.json():
        quotes.append(Quote(quote))
    return quotes