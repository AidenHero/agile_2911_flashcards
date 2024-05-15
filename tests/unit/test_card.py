import pytest
from models import Flashcard
from db import db
from app import app
from sqlalchemy.exc import IntegrityError

def test_validate_new_card():
    new_card = Flashcard(
        flash_id=15,
        question="How to set up a trial card?",
        answer="Trial answer", 
        set_id=1
    )

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

def test_validate_new_card_missing_inputs():        
    with pytest.raises(IntegrityError):
        new_card = Flashcard() # missing input data 
        with app.app_context():
            db.session.add(new_card)
            db.session.commit()


