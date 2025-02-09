from supabase import create_client, Client
from .exceptions import InsufficientFundsException
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

# Secure versions of delete and update functions, check prior to evade concurrency errors
def secure_delete_portfolio(user_id: str, ticker: str, prior_ammount: int)-> None:
    return client.table("porfolio").delete()\
                                    .eq("user_id", user_id)\
                                    .eq("ticker", ticker)\
                                    .eq("ammount", prior_ammount).execute()
def secure_update_portfolio(user_id: str, ticker: str, ammount, prior_ammount: int)-> None:
    return client.table("porfolio").update({"ammount": ammount})\
                                    .eq("user_id", user_id)\
                                    .eq("ticker", ticker)\
                                    .eq("ammount", prior_ammount)\
                                    .execute()

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
        secure_update_portfolio(user_id,ticker,ammount+stock_available, stock_available)

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
    if difference < 0:
        # not enough stock to delete
        raise InsufficientFundsException()
    if difference == 0:
        # delete from the database because its not used
        secure_delete_portfolio(user_id,ticker,stock_available)
    else:
        # update value
        secure_update_portfolio(user_id,ticker,difference, stock_available)

    # return the ammount of stock deleted
    return difference if difference > 0 else ammount + difference

# Locks to ensure ACID transactions
def lock_transactions(user_id: str):
    client.table("locks").insert({"user_id": user_id}).execute()
def unlock_transactions(user_id: str):
    client.table("locks").delete().eq("user_id",user_id).execute()


# Create bussines functions
def buy_stock(user_id: str, ticker: str, ammount: int, price: int) -> bool:
    """
        Buys an ammount of stock using the users money
        The money must be in cents.
        Returns: True if transaction success and false if inssuficient funds
        Exception: Concurrent error
    """
    # there has to be some kind of finnaly to evade errors
    
    lock_transactions(user_id)
    try:
        # get available cash
        cash = get_portfolio_ticker(user_id,settings.MONEY_TICKER)
        if cash < price*ammount:
            return False
        # remove cash
        remove_stock(user_id,settings.MONEY_TICKER, price*ammount)
        # add stock
        add_stock(user_id,ticker, ammount)
    finally:
        unlock_transactions(user_id)

    return True

def sell_stock(user_id: str, ticker: str, ammount: int, price: int) -> bool:
    """
        Sells the ammount of stock for cents.
        The money must be in cents.
        Returns: True if transaction success and false if inssuficient stock
        Exception: Concurrent error
    """
    lock_transactions(user_id)
    try:
        # get available stock
        stock = get_portfolio_ticker(user_id,ticker)
        # remove stock
        remove_stock(user_id,ticker,ammount)
        # add cash
        add_stock(user_id,settings.MONEY_TICKER, ammount*price)

    finally:
        unlock_transactions(user_id)

    return stock < ammount