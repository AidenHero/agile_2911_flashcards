from app import app
from db import db
from models import Flashcard
def test_create_cards_page():
    with app.test_client() as test_client:
        response = test_client.get("/cards/")
        assert response.status_code == 200
        assert b'Choose a set' in response.data


    req_values = ['card_question', 'card_answer', 'card_set']
def test_create_cards_post():
    with app.test_client() as test_client:
        response = test_client.post("/cards/", data = {
            'card_question': "this is a test",
            'card_answer': 'this is still a test',
            'card_set': 2
            })

        flashcardtest = db.session.execute(db.select(Flashcard).where(Flashcard.question == "this is a test")).scalar()
        db.session.delete(flashcardtest)
        db.session.commit()
        assert response.status_code == 302