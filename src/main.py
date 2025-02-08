from typing import Union

from fastapi import FastAPI, HTTPException, Depends
from .data_models import TickerValuation
from . import operations
import logging
from .settings import settings
from .controllers import auth, portfolio
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("main")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# Include routers from different controller files
app.include_router(auth.router, prefix="", tags=["Auth"])
app.include_router(portfolio.router, prefix="", tags=["Products"])