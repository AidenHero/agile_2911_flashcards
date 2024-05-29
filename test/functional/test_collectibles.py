from app import app
from db import db
from models import Customer
from werkzeug.security import check_password_hash
import requests
import pytest

@pytest.fixture()
def client():
    return app.test_client()

@pytest.fixture() 
def context():
     return app.app_context()

def test_collectibles_page(client, context):
    with context: 
        response = client.post("/register", data = {
            'register_name': 'Test Name',
            'register_username': "Test Username",
            'register_password': 'Test Password',
        })

        response = client.post("/login", data = {
            'loginusername': 'Test Username',
            'loginPassword': "Test Password"
        })

        response = client.get("/collectibles/buy")
        assert response.status_code == 200
        assert b"Not enough points to get a collectible" in response.data 

        retrieved_customer = db.session.execute(db.select(Customer).where(Customer.username == "Test Username")).scalar()

        db.session.delete(retrieved_customer)
        db.session.commit()

