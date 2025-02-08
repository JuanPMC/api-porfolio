from . import providers
import logging
from fastapi import HTTPException

logger = logging.getLogger("main")

def get_ticker_value(ticker: str) -> float:
    response_code, response  = providers.get_stock_price(ticker)
    logger.info(f"RESPONSE:{response} CODE: {response_code} TICKER: {ticker}")
    if not response["Global Quote"].get("05. price"):
        raise HTTPException(404,"Ticker could not be found")
    return float(response["Global Quote"]["05. price"])