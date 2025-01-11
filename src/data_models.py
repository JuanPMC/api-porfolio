from pydantic import BaseModel
from enum import Enum

class TickerValuation(BaseModel):
    value: float

class Ticker(str,Enum):
    MSFT = "msft"
    GOOP = "goop"
    NVDA = "nvda"