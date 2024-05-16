from app import app
from db import db
from models import Flashcard_set

def test_display_sets_page(): # checks if the page displays
    with app.test_client() as test_client:
        response = test_client.get("/all/sets/")
        assert response.status_code == 200
        assert b'All Sets' in response.data
        assert b'Update Set' in response.data
        assert b'Delete Set' in response.data

def test_display_sets_create_page(): # checks if the create set page displays
    with app.test_client() as test_client:
        response = test_client.get("/sets/create")
        assert response.status_code == 200
        assert b'Create a New Set' in response.data
        assert b'Set Title' in response.data
        assert b'Set Description' in response.data
        assert b'Create' in response.data

def test_display_sets_update_page(): # checks if the update set page displays
    with app.test_client() as test_client:
        response = test_client.get("/sets/1/update")
        retrieved_set = db.session.execute(db.select(Flashcard_set).where(Flashcard_set.set_id == 1)).scalar()
   
        assert response.status_code == 200
        assert b'Edit Set' in response.data
        assert retrieved_set.name == "agile" 
        assert retrieved_set.description == None
        assert retrieved_set.customer_id == 1


def test_create_set_post(): # checks if set posts successfully 
    with app.test_client() as test_client:
        response = test_client.post("/sets/create", data = {
            'set_name': "Test Set Name",
            'set_descript': 'Test Set Description',
        })
        retrieved_set = db.session.execute(db.select(Flashcard_set).where(Flashcard_set.name == "Test Set Name")).scalar()
        assert retrieved_set.name == "Test Set Name" 
        assert retrieved_set.description == "Test Set Description"
        assert response.status_code == 200

        db.session.delete(retrieved_set)
        db.session.commit()