from db import db
from app import app
from models import Customer, Flashcard, Flashcard_set
from csv import DictReader
from sqlalchemy.sql import functions as func
import random
from werkzeug.security import generate_password_hash, check_password_hash


def create_customer_database():
    with open("data/customers.csv", 'r') as csvfile:
        reader = DictReader(csvfile)
        reader1=(list(reader))
        for row in reader1:
            hashed_password = generate_password_hash(row['password'])
            obj = Customer(name=row['name'], username=row['username'], password=hashed_password)
            db.session.add(obj)
        db.session.commit()

def create_flashcard_set_database():
    with open("data/flashcard_sets.csv", newline="") as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            obj = Flashcard_set(name=row['name'], customer_id=int(row['customer_id']))
            db.session.add(obj)
        db.session.commit()

def create_flashcard_database():
    with open("data/flashcards.csv", newline="") as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            obj = Flashcard(question=row['question'], answer=row['answer'], set_id=int(row['set_id']))
            db.session.add(obj)
        db.session.commit()

# def drop_table():
#     with app.app_context():
#         db.drop_all()

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        create_customer_database()
        create_flashcard_set_database()
        create_flashcard_database()