from fastapi import APIRouter, Depends
from .auth import get_user_info
from ..data_models import TickerValuation
from .. import operations


router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.get("/value/{ticker}")
async def get_ticker_value(ticker: str) -> TickerValuation:

    value: float = operations.get_ticker_value(ticker)

    return TickerValuation(value=value)

@router.get("/protected")
async def protected_route(current_user: dict = Depends(get_user_info)):
    return {"message": "You have accessed a protected route!", "user": current_user}