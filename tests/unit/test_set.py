import pytest
from models import Customer, Flashcard_set
from db import db
from app import app
from sqlalchemy.exc import IntegrityError

def test_validate_new_set():
    new_set = Flashcard_set(
        set_id=15,
        name="Trial Set",
        customer_id=1
    )

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

def test_validate_new_set_missing_inputs():        
    with pytest.raises(IntegrityError):
        new_set = Flashcard_set() # missing input data 
        with app.app_context():
            db.session.add(new_set)
            db.session.commit()


