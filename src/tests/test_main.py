from fastapi.testclient import TestClient
from mockito import when, unstub
from src.main import app
from src import providers
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def unstub_after_test():
    """
    Automatically unstubs all mocked methods after each test.
    """
    yield
    unstub()

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() ==  {"Hello": "World"}

def test_value_ticker():
    when(providers).get_stock_price("msft").thenReturn((200,{"Global Quote":{"05. price":3.2}}))
    response = client.get("/value/msft")
    assert response.status_code == 200
    assert response.json() ==  {"value": 3.2}