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

@pytest.fixture()
def to_login(client):
    return client.post("login", data={
            'loginusername': "AidenHero",
            'loginPassword': "aiden123"
        })

def test_display_homepage(client): # checks if the homepage displays
    with client:
        response = client.get("/")
        assert response.status_code == 200
        assert b'Home' in response.data

def test_display_login(client): # checks if the login page displays
    with client:
        response = client.get("/login")
        assert response.status_code == 200
        assert b'Login' in response.data
        assert b'Username' in response.data
        assert b'Password' in response.data

def test_display_register(client): # checks if the register displays
    with client:
        response = client.get("/register")
        assert response.status_code == 200
        assert b'Register' in response.data
        assert b'Username' in response.data
        assert b'Password' in response.data


def test_register_post(): # checks if register posts successfully 
    with app.test_client() as test_client:
        response = test_client.post("/register", data = {
            'register_name': 'Test Name',
            'register_username': "Test Username",
            'register_password': 'Test Password',
        })
        retrieved_customer = db.session.execute(db.select(Customer).where(Customer.username == "Test Username")).scalar()
        assert retrieved_customer.name == "Test Name" 
        assert retrieved_customer.username == "Test Username"
        assert check_password_hash(retrieved_customer.password, 'Test Password')
        assert response.status_code == 302

        db.session.delete(retrieved_customer)
        db.session.commit()
