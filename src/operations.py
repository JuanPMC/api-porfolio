from .data_models import Ticker
from . import providers
import logging

logger = logging.getLogger("main")

def get_ticker_value(ticker: Ticker) -> float:
    response: dict = providers.get_stock_price(ticker.value)
    logger.info(f"RESPONSE:{response} TICKER: {ticker.value}")
    return float(response["Global Quote"]["05. price"])