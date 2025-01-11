from typing import Union

from fastapi import FastAPI
from .data_models import TickerValuation, Ticker
from . import operations

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/value/{ticker}")
async def get_ticker_value(ticker: Ticker) -> TickerValuation:

    value: float = operations.get_ticker_value(ticker)

    return TickerValuation(value=value)