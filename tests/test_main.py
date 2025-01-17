from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() ==  {"Hello": "World"}


def test_value_ticker():
    response = client.get("/value/msft")
    assert response.status_code == 200
    assert response.json() ==  {"value": 3.2}