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


def test_register_post(client): # checks if register posts successfully 
    with client:
        response = client.post("/register", data = {
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

def test_login_invalid_username(client): # checks if the login system rejects invalid username (not registered)
    with client:
        response = client.post("/login", data = {
            'loginusername': 'Test Username',
            'loginPassword': "Test Password"
        })

        retrieved_customer = db.session.execute(db.select(Customer).where(Customer.username == "Test Username")).scalar()

        with pytest.raises(AttributeError): # checks that non-existant username login will raise error 
            assert retrieved_customer.username == "Test Username"

def test_login_valid_username(client): # checks if the login system works with registered customer/username
    with client:
        response = client.post("/login", data = {
            'loginusername': 'AidenHero',
            'loginPassword': "aiden123"
        })

        assert response.status_code == 302
        assert response.headers['Location'] == '/' # checks redirected to homepage


def test_login_invalid_password(client): # checks if the login page rejects invalid password for registered user
    with client:
        response = client.post("/login", data = {
            'loginusername': 'AidenHero',
            'loginPassword': "testing"
        })

        assert response.status_code == 200
        assert b"Invalid password" in response.data 


def test_register_duplicate_username(client): # checks if duplicate username registration is rejected
    with client:
        response = client.post("/register", data = {
            'register_name': 'Test Name',
            'register_username': "AidenHero",
            'register_password': 'TestPassword'
        })

        assert response.status_code == 200
        assert b"Username already exists" in response.data 

def test_register_missing_fields(client): # checks if error when user doesn't fill in all the registration info
    with client:
        response = client.post("/register", data = {
            'register_name': 'Test Name'
        })

        assert response.status_code == 200
        assert b"not all fields were filled" in response.data 

def test_logout(client, to_login):
    to_login
    with client: 
        response = client.get("/logout")
        assert response.status_code == 302
        assert response.headers['Location'] == '/login' 