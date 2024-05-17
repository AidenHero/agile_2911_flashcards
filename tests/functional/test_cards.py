from app import app
from db import db
from models import Flashcard_set, Customer, Flashcard
import pytest
from flask_login import login_user, login_required

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



def test_card_creation(client, context, to_login):
    to_login
    response = client.post("/cards/", data={
        'card_question': 'this is a test',
        'card_answer': 'this is an answer',
        'card_set': 2
    })
    assert response.status_code == 302

    with context:
        new_card = db.session.execute(db.select(Flashcard).where(Flashcard.question == "this is a test")).scalar()
        assert new_card.question == "this is a test"
        db.session.delete(new_card)
        db.session.commit()

def test_card_creation_fail(client, to_login):
    to_login
    response = client.post("/cards/", data={
        'card_question': 'this shouldnt work',
    })
    assert response.status_code == 400
    assert b'ERR: INVALID ARGS' in response.data

    response = client.post('/cards/', data={
        'card_question': 'this shouldnt woork',
        'card_answer': 'because of the set',
        'card_set': 'a'
    })

    assert response.status_code == 400
    assert b'ERR: INVALID SET DATA' in response.data
    
    response = client.post('/cards/', data={
        'card_question': 'this shouldnt work',
        'card_answer': 'because the set doesnt exist',
        'card_set': 200
    })

    assert response.status_code == 404

def test_card_updating(client, context, to_login):
    to_login
    response = client.post("/cards/", data={
        'card_question': 'this is a test',
        'card_answer': 'this is an answer',
        'card_set': 2
    })
    response = client.post("/cards/7/update", data={
        'new_question': 'what is this doing?',
        'new_answer': 'this is updating'
    })
    assert response.status_code == 302
    with context:
        updated_card = db.session.execute(db.select(Flashcard).where(Flashcard.flash_id == 7)).scalar()
        assert updated_card.question == "what is this doing?"
        assert updated_card.answer == "this is updating"


    response = client.post("/cards/7/update", data={
        'new_question': 'only question updated'
    })
    assert response.status_code == 302
    with context:
        updated_card = db.session.execute(db.select(Flashcard).where(Flashcard.flash_id == 7)).scalar()
        assert updated_card.question == "only question updated"
        assert updated_card.answer == "this is updating"

    response = client.post("/cards/7/update", data={
        'new_answer': 'now answer has updated'
    })

    with context:
        updated_card = db.session.execute(db.select(Flashcard).where(Flashcard.flash_id == 7)).scalar()
        assert updated_card.question == "only question updated"
        assert updated_card.answer == "now answer has updated"
        db.session.delete(updated_card)
        db.session.commit()

def test_card_updating_fail(client, to_login):
    to_login
    response = client.post('/cards/404/update',data={
        "new_answer": "this card doesn't exist"
        })
    
    assert response.status_code == 404

def test_card_deleting(client, context, to_login):
    to_login
    client.post("/cards/", data={
        'card_question': 'this is a test',
        'card_answer': 'this is an answer',
        'card_set': 2
    })

    response = client.post('/cards/7/delete')

    assert response.status_code == 302

    with context:
        card = db.session.execute(db.select(Flashcard).where(Flashcard.flash_id == 7)).scalar()

        assert card == None

def test_card_deleting_fail(client, to_login):
    to_login
    response = client.post('/cards/404/delete')
    assert response.status_code == 404

def test_card_screen(client, to_login):
    to_login
    response = client.get("/cards/")
    print(response.data)
    assert response.status_code == 200

    assert b'The Question' in response.data
    assert b'The Answer' in response.data

