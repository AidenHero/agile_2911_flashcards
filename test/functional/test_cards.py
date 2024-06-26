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

def test_display_cards_page(client, to_login): # checks if the all cards page displays
    to_login
    response = client.get("/all/cards/")
    assert response.status_code == 200

def test_display_specific_card_page(client, to_login):
    to_login
    response = client.get("/all/cards/1") # checks if page for specific card displays
    assert b'Question' in response.data
    assert b'Answer' in response.data
        
# def test_display_answers_page(client, to_login): # checks if answers page displays
#     to_login
#     response = client.get("/all/cards/answer")
#     assert b'Your answer' in response.data

#we will come back to this later OOPSY

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
    # response = client.post("/cards/", data={
    #     'card_question': 'this is a test',
    #     'card_answer': 'this is an answer',
    #     'card_set': 2
    # })

    with context:
        new_card = Flashcard(flash_id=888, question="Testing Card", answer="Testing Card Answer", set_id=1)
        db.session.add(new_card)
        db.session.commit()

    response = client.post("/cards/888/update", data={
        'new_question': 'what is this doing?',
        'new_answer': 'this is updating'
    })
    assert response.status_code == 302
    with context:
        updated_card = db.session.execute(db.select(Flashcard).where(Flashcard.flash_id == 888)).scalar()
        assert updated_card.question == "what is this doing?"
        assert updated_card.answer == "this is updating"


    response = client.post("/cards/888/update", data={
        'new_question': 'only question updated'
    })
    assert response.status_code == 302
    with context:
        updated_card = db.session.execute(db.select(Flashcard).where(Flashcard.flash_id == 888)).scalar()
        assert updated_card.question == "only question updated"
        assert updated_card.answer == "this is updating"

    response = client.post("/cards/888/update", data={
        'new_answer': 'now answer has updated'
    })

    with context:
        updated_card = db.session.execute(db.select(Flashcard).where(Flashcard.flash_id == 888)).scalar()
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
    # client.post("/cards/", data={
    #     'card_question': 'this is a test',
    #     'card_answer': 'this is an answer',
    #     'card_set': 2
    # })

    # response = client.post('/cards/7/delete')

    # assert response.status_code == 302

    # with context:
    #     card = db.session.execute(db.select(Flashcard).where(Flashcard.flash_id == 7)).scalar()

    #     assert card == None

    with context:
        new_card = Flashcard(flash_id=888, question="Testing Card", answer="Testing Card Answer", set_id=1)
        db.session.add(new_card)
        db.session.commit()

    response = client.post('/cards/888/delete')

    assert response.status_code == 302

    with context:
        card = db.session.execute(db.select(Flashcard).where(Flashcard.flash_id == 888)).scalar()

        assert card == None

def test_card_deleting_fail(client, to_login):
    to_login
    response = client.post('/cards/404/delete')
    assert response.status_code == 404


def test_card_updating_not_logged_in(client):
    response = client.get("/cards/")
    assert response.status_code == 302

def test_card_screen(client, to_login):
    to_login
    response = client.get("/cards/")
    print(response.data)
    assert response.status_code == 200

    assert b'The Question' in response.data
    assert b'The Answer' in response.data


## Test quiz features
def test_view_quiz(client, to_login):
    to_login
    response = client.get("/all/cards/quiz/1")
    assert response.status_code == 200

def test_quiz_another_user_set(client): # tests if someone enters set manually into URL that's not their set
    client.post("login", data={
        'loginusername': "asdf",
        'loginPassword': "aiden123"
    })
    
    response = client.get("/all/cards/quiz/1")
    assert b'You are not permitted to view this set' in response.data


## Test answers 

def test_answer_invalid_set(client): #tests you get error if you try to view set that does not exist 
    response = client.get("/answer/90")
    assert response.status_code == 404
    # assert b'You are not permitted to view this set.' in response.data

def test_answer_without_card(client, to_login, context): # tests there will be a prompt that there's no card in set
    to_login
    with context:
        new_set = Flashcard_set(set_id=888, name="Testing Set", customer_id=1, description="Testing Set Description")
        db.session.add(new_set)
        db.session.commit()

        response = client.get("/all/cards/answer/888")
        assert b'No cards in this set' in response.data

        retrieved_set = db.session.execute(db.select(Flashcard_set).where(Flashcard_set.set_id == 888)).scalar()
        db.session.delete(retrieved_set)
        db.session.commit() 

def test_answer_another_user_set(client): # tests if someone enters set manually into URL that's not their set
    client.post("login", data={
        'loginusername': "asdf",
        'loginPassword': "aiden123"
    })
    
    response = client.get("/all/cards/answer/1")
    assert b'You are not permitted to view this set' in response.data

