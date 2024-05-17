from app import app
from db import db
from models import Flashcard_set, Customer
import pytest
from flask_login import login_user, login_required


def test_display_sets_page(): # checks if the all sets page displays
    with app.test_client() as test_client:
        test_client.post("/login", data = {
            'loginusername': "AidenHero",
            'loginPassword': "aiden123"
        })

        response = test_client.get("/all/sets/")
        assert response.status_code == 200
        assert b'All Sets' in response.data
        assert b'Update Set' in response.data
        assert b'Delete Set' in response.data

def test_display_sets_create_page(): # checks if the create set page displays
    with app.test_client() as test_client:
        test_client.post("/login", data = {
            'loginusername': "AidenHero",
            'loginPassword': "aiden123"
        })
                
        response = test_client.get("/sets/create")
        assert response.status_code == 200
        assert b'Create a New Set' in response.data
        assert b'Set Title' in response.data
        assert b'Set Description' in response.data
        assert b'Create' in response.data

def test_display_sets_update_page(): # checks if the update set page displays
    with app.test_client() as test_client:
        test_client.post("/login", data = {
            'loginusername': "AidenHero",
            'loginPassword': "aiden123"
        })
        response = test_client.get("/sets/1/update")
        retrieved_set = db.session.execute(db.select(Flashcard_set).where(Flashcard_set.set_id == 1)).scalar()
   
        assert response.status_code == 200
        assert b'Edit Set' in response.data
        assert retrieved_set.name == "agile" 
        assert retrieved_set.description == None
        assert retrieved_set.customer_id == 1


def test_create_set_post(): # checks if set posts successfully 
    with app.test_client() as test_client:
        test_client.post("/login", data = {
            'loginusername': "AidenHero",
            'loginPassword': "aiden123"
        })

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

def test_update_and_delete_set_post(): # checks if set updates and deletes successfully 
    with app.test_client() as test_client:
        test_client.post("/login", data = {
            'loginusername': "AidenHero",
            'loginPassword': "aiden123"
        })
        
        with app.app_context():
            new_set = Flashcard_set(set_id=88, name="Testing Set", customer_id=1, description="Testing Set Description")
            db.session.add(new_set)
            db.session.commit()

        response = test_client.post("sets/88/update", data = { # update set
            'updated_name': "New Test Set Name",
            'updated_descrp': 'New Test Set Description',
        })
        retrieved_set = db.session.execute(db.select(Flashcard_set).where(Flashcard_set.set_id == 88)).scalar()

        assert retrieved_set.name == "New Test Set Name" 
        assert retrieved_set.description == "New Test Set Description"
        assert response.status_code == 302

        
        response = test_client.post("sets/88/update") # update set without new inputs. Make sure it's still the input from before

        retrieved_set = db.session.execute(db.select(Flashcard_set).where(Flashcard_set.set_id == 88)).scalar()

        assert retrieved_set.name == "New Test Set Name" 
        assert retrieved_set.description == "New Test Set Description"


        response = test_client.post("sets/88/delete")  # delete set
        assert response.status_code == 302
        assert retrieved_set.description == "New Test Set Description"

        response = test_client.post("sets/8888/delete")  # nonexistant
        assert response.status_code == 404
