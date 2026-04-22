from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Servidor activo"}

def test_divide_ok():
    response = client.get("/divide?a=10&b=2")
    assert response.status_code == 200
    assert response.json()["result"] == 5

def test_divide_zero():
    response = client.get("/divide?a=10&b=0")
    assert response.status_code == 500

def test_square_ok():
    response = client.get("/square?x=4")
    assert response.status_code == 200
    assert response.json()["result"] == 16

def test_square_negative():
    response = client.get("/square?x=-3")
    assert response.status_code == 500