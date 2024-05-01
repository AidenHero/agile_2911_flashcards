from sqlalchemy import Float, Numeric, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import functions as func
from datetime import datetime

from db import db

class Customer(db.Model):
    id = mapped_column(Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

class Flashcard_set(db.Model):
    set_id=mapped_column(Integer, primary_key=True)

class Flashcard(db.Model):
    flash_id=mapped_column(Integer, primary_key=True)