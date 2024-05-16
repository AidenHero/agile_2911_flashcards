import pytest
from models import Customer
from db import db
from app import app
from sqlalchemy.exc import IntegrityError

def test_validate_new_customer():
    new_cust = Customer(
        id=15,
        name="Mary Test",
        username="Mary_Test",
        password="Hello123"
    )

    with app.app_context():
        db.session.add(new_cust)
        db.session.commit()
        retrieved_cust = db.session.execute(db.select(Customer).where(Customer.id == new_cust.id)).scalar()

    assert retrieved_cust.name == "Mary Test"
    assert retrieved_cust.username == "Mary_Test"
    assert retrieved_cust.password == "Hello123"

    with app.app_context():
        db.session.delete(retrieved_cust)
        db.session.commit()

def test_validate_new_customer_missing_inputs():
    new_cust = Customer(
        id=15,
        name="Mary Test",
        username="Mary_Test",
        password="Hello123"
    )
        
    with pytest.raises(IntegrityError):
        new_cust = Customer() # missing input data 
        with app.app_context():
            db.session.add(new_cust)
            db.session.commit()


