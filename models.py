from sqlalchemy import Float, Numeric, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import functions as func
from datetime import datetime

from db import db

class Customer(db.Model):
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(200), nullable=False)
    username = mapped_column(String(100), nullable=False, unique=True)
    password = mapped_column(String(100), nullable=False)
    set = relationship("Flashcard_set", back_populates="customer", cascade="all, delete-orphan")
    
    # def to_json(self):
    #  return {
    #      'id': self.id,
    #      'name': self.name,
    #      'phone': self.phone,
    #      'balance': self.balance
    #      }

class Flashcard_set(db.Model):
    set_id=mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(200), nullable=False)
    customer_id = mapped_column(Integer, ForeignKey(Customer.id), nullable=False)
    customer = relationship("Customer", back_populates="set")
    card = relationship("Flashcard", back_populates="set", cascade="all, delete-orphan")

class Flashcard(db.Model):
    flash_id=mapped_column(Integer, primary_key=True, autoincrement=True)
    question = mapped_column(String(500), nullable=False)
    answer = mapped_column(String(500), nullable=False)
    set_id = mapped_column(Integer, ForeignKey(Flashcard_set.set_id), nullable=False)
    set = relationship("Flashcard_set", back_populates="card")
