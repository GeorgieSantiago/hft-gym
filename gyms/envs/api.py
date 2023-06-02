import requests
from models.prices import Price
from models.quote import Quote

BASE_URL = "http://127.0.0.1:8000/api"

def get_price_history(symbol: str) -> list[Price]:
    # A GET request to the API
    response: requests.Response = requests.get(f"{BASE_URL}/price/history/{symbol}")
    prices = list()
    # Print the response
    for data in response.json():
        prices.append(Price(data))
    return prices

def get_quote(symbol: str) -> Quote:
    response: requests.Response = requests.get(f"{BASE_URL}/qoute/{symbol}")
    return Quote(response.json())
