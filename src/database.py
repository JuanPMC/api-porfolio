from supabase import create_client, Client
from .settings import settings

# Make the client available for all methods
client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


# Create simple CRUD methods
def insert_to_portfolio(user_id: str, ticker: str, ammount: int) -> None:
    return client.table("porfolio").insert({"user_id": user_id, "ticker": ticker, "ammount": ammount}).execute()

def delete_portfolio(user_id: str, ticker: str)-> None:
    return client.table("porfolio").delete().eq("user_id", user_id).eq("ticker", ticker).execute()

def update_portfolio(user_id: str, ticker: str, ammount)-> None:
    return client.table("porfolio").update({"ammount": ammount}).eq("user_id", user_id).eq("ticker", ticker).execute()

def get_portfolio_ticker(user_id: str, ticker: str) -> int:
    result = client.table("porfolio").select(["ticker, ammount"]).eq("user_id", user_id).eq("ticker", ticker).execute()
    if result.data:
        return result.data[0]["ammount"]
    return 0

def get_user_portfolio(user_id: str)-> list:
    result = client.table("porfolio").select(["ticker, ammount"]).eq("user_id", user_id).execute()
    return result.data

# Create higher level functions

# add stock
def add_stock(user_id: str, ticker: str, ammount: int):
    assert ammount > 0
    # Get the current stock ammount
    stock_available: int = get_portfolio_ticker(user_id,ticker)
    # If not exist
    if stock_available == 0:
        insert_to_portfolio(user_id,ticker,ammount)
    else:
        update_portfolio(user_id,ticker,ammount+stock_available)

# remove stock
def remove_stock(user_id: str, ticker: str, ammount: int) -> int:
    """
        Will remove available stock. It will return the deleted stock,
        It can only delete as much as the user has.
    """
    # Get current stock
    stock_available: int = get_portfolio_ticker(user_id,ticker)
    # Get the difference
    difference: int = stock_available - ammount
    if difference <= 0:
        # delete stock
        delete_portfolio(user_id,ticker)
    else:
        # update value
        update_portfolio(user_id,ticker,difference)

    # return the ammount of stock deleted
    return difference if difference > 0 else ammount + difference

# Create bussines functions
def buy_stock(user_id: str, ticker: str, ammount: int, price: float):
    # there has to be some kind of finnaly to evade errors

    # get available cash
    # if insufficient:
        # return false
    # remove cash
    # add stock
    # return true

def sell_stock(user_id: str, ticker: str, ammount: int, price: float):
    # there has to be some kind of finnaly to evade errors

    # get available stock
    # if not sufficient
        # return false
    # remove stock
    # remove cash
    # return true