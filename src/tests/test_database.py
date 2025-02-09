from ..database import insert_to_portfolio, delete_portfolio, update_portfolio, get_portfolio_ticker, get_user_portfolio

def test_insert_portfolio():
    insert_to_portfolio("1234", "testing", 100)

    result = get_portfolio_ticker("1234","testing")
    
    assert result == 100, result

    delete_portfolio("1234","testing")

def test_update_portfolio():
    insert_to_portfolio("1234", "testing", 100)
    update_portfolio("1234", "testing", 50)

    result = get_portfolio_ticker("1234","testing")

    assert result == 50, result

    delete_portfolio("1234","testing")

def test_get_user_porfolio():
    insert_to_portfolio("1234", "testing", 100)
    insert_to_portfolio("1234", "testing2", 100)

    result = get_user_portfolio("1234")

    assert len(result) >= 2, result

    delete_portfolio("1234","testing")
    delete_portfolio("1234","testing2")

def test_select_unexisting():
    result = get_portfolio_ticker("1234","picolo")
    assert result==0, result