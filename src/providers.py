from .settings import settings
import requests

def get_stock_price(ticker: str) -> tuple[int,dict]:
    url : str = f'{settings.ALPHAVANTAGE_URL}query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={settings.ALPHAVANTAGE_APIKEY}'
    response: requests.Response = requests.get(url,timeout=5)
    return response.status_code ,response.json()
