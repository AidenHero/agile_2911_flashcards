from app import app
from db import db
from models import Customer

def test_display_homepage(): # checks if the homepage displays
    with app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 200
        assert b'Home' in response.data

def test_display_login(): # checks if the login page displays
    with app.test_client() as test_client:
        response = test_client.get("/login")
        assert response.status_code == 200
        assert b'Login' in response.data
        assert b'Username' in response.data
        assert b'Password' in response.data

def test_display_register(): # checks if the register displays
    with app.test_client() as test_client:
        response = test_client.get("/register")
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
        assert retrieved_customer.password == "Test Password"
        assert response.status_code == 200

        db.session.delete(retrieved_customer)
        db.session.commit()
