from pydantic import BaseModel
from enum import Enum

class TickerValuation(BaseModel):
    value: float