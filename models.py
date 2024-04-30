from sqlalchemy import Float, Numeric, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import functions as func
from datetime import datetime

from db import db

class Customer(db.Model):
    id = mapped_column(Integer, primary_key=True)
    # name = mapped_column(String(200), nullable=False, unique=True)
    # phone = mapped_column(String(20), nullable=False)
    # def to_json(self):
    #  return {
    #      'id': self.id,
    #      'name': self.name,
    #      'phone': self.phone,
    #      'balance': self.balance
    #      }

class Flashcard_set(db.Model):
    set_id=mapped_column(Integer, primary_key=True)

class Flashcard(db.Model):
    flash_id=mapped_column(Integer, primary_key=True)