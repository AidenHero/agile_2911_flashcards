import pytest
from models import Customer, Flashcard_set
from db import db
from app import app
from sqlalchemy.exc import IntegrityError

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
    # assert retrieved_set.customer.username == "AidenHero"

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
        new_set = Flashcard_set(set_id=15,customer_id=1) # missing input data 
        with app.app_context():
            db.session.add(new_set)
            db.session.commit()

