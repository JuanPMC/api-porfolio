from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TickerValuation(BaseModel):
    value: float



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/value/{ticker}")
async def get_ticker_value(ticker: str) -> TickerValuation:
    return TickerValuation(value=3.2)