import pytest
from models import Flashcard, Customer, Flashcard_set
from db import db
from app import app
from sqlalchemy.exc import IntegrityError

# Tests for cards

@pytest.fixture(scope="module") # fixture for a new card
def new_card():
    new_card2 = Flashcard(
        flash_id=15,
        question="How to set up a trial card?",
        answer="Trial answer", 
        set_id=1
    )
    return new_card2

def test_validate_new_card(new_card): # test if new card is added correctly 
    with app.app_context():
        db.session.add(new_card)
        db.session.commit()
        retrieved_card = db.session.execute(db.select(Flashcard).where(Flashcard.flash_id == new_card.flash_id)).scalar()

    assert retrieved_card.flash_id == 15
    assert retrieved_card.question == "How to set up a trial card?"
    assert retrieved_card.answer == "Trial answer"
    assert retrieved_card.set_id == 1

    with app.app_context():
        db.session.delete(retrieved_card)
        db.session.commit()

def test_validate_new_card_missing_inputs():  # checks that you cannot create a new card with missing info      
    with pytest.raises(IntegrityError):
        new_card = Flashcard() # missing input data 
        with app.app_context():
            db.session.add(new_card)
            db.session.commit()


# tests for customers


def test_validate_new_customer_missing_inputs():# checks cannot add customer with missing inputs
    with pytest.raises(IntegrityError):
        new_cust = Customer() # missing input data 
        with app.app_context():
            db.session.add(new_cust)
            db.session.commit()

def test_validate_new_customer_missing_name():# checks cannot add customer with missing name
    with pytest.raises(IntegrityError):
        new_cust = Customer(
            id=15,
            username="Mary_Test",
            password="Hello123"
        )
        with app.app_context():
            db.session.add(new_cust)
            db.session.commit()

def test_validate_new_customer_duplicate_username(): # cannot add customer with duplicate username
    with pytest.raises(IntegrityError):
        new_cust = Customer(
            name="Aiden",
            username="AidenHero", # duplicate
            password="Hello123"
        )
        with app.app_context():
            db.session.add(new_cust)
            db.session.commit()


@pytest.fixture(scope="module") # fixture for new customer
def new_cust(): 
    new_cust2 = Customer(
        id=15,
        name="Mary Test",
        username="Mary_Test",
        password="Hello123"
    )
    return new_cust2

def test_validate_new_customer(new_cust): # checks a new customer gets added correctly 
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


# tests for sets

@pytest.fixture(scope="module")
def new_set(): 
    new_set2 = Flashcard_set(
        set_id=15,
        name="Trial Set",
        customer_id=1
    )
    return new_set2

def test_validate_new_set(new_set): # check new set is made correctly 
    with app.app_context():
        db.session.add(new_set)
        db.session.commit()
        retrieved_set = db.session.execute(db.select(Flashcard_set).where(Flashcard_set.set_id == new_set.set_id)).scalar()

    assert retrieved_set.set_id == 15
    assert retrieved_set.name == "Trial Set"
    assert retrieved_set.customer_id == 1

    with app.app_context():
        db.session.delete(retrieved_set)
        db.session.commit()

def test_validate_new_set_missing_info(): # checks cannot add new set with missing info
    with pytest.raises(IntegrityError):
        new_set = Flashcard_set() # missing input data 
        with app.app_context():
            db.session.add(new_set)
            db.session.commit()

def test_validate_new_set_missing_name(): # checks cannot add new set with missing set name  
    with pytest.raises(IntegrityError):
        new_set = Flashcard_set(set_id=15,customer_id=1) # missing name 
        with app.app_context():
            db.session.add(new_set)
            db.session.commit()

