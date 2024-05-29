from sqlalchemy import Float, Numeric, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import functions as func
from datetime import datetime
from flask_login import UserMixin

from db import db

class Customer(UserMixin, db.Model):
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(200), nullable=False)
    username = mapped_column(String(250), nullable=False, unique=True)
    password = mapped_column(String(250), nullable=False)
    points = mapped_column(Integer, nullable=False, default=0)
    set = relationship("Flashcard_set", back_populates="customer", cascade="all, delete-orphan")


class Flashcard_set(db.Model):
    set_id=mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(200), nullable=False)
    customer_id = mapped_column(Integer, ForeignKey(Customer.id), nullable=False) 
    description = mapped_column(String(200), nullable=True)
    customer = relationship("Customer", back_populates="set")
    card = relationship("Flashcard", back_populates="set", cascade="all, delete-orphan")

class Flashcard(db.Model):
    flash_id=mapped_column(Integer, primary_key=True, autoincrement=True)
    question = mapped_column(String(500), nullable=False)
    answer = mapped_column(String(500), nullable=False)
    set_id = mapped_column(Integer, ForeignKey(Flashcard_set.set_id), nullable=False)
    tags = mapped_column(String(200), nullable=True)
    priority = mapped_column(Integer, nullable=False, default=1)
    last_seen = mapped_column(DateTime, nullable=True)
    last_result = mapped_column(Integer, nullable = True)
    time_created = mapped_column(DateTime, nullable=True)
    time_updated = mapped_column(DateTime, nullable=True)
    set = relationship("Flashcard_set", back_populates="card")

class Collectible(db.Model):
    collectible_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(500), nullable=False)
    description = mapped_column(String(500), nullable=False)

class Customer_Owned_Collectible(db.Model):
    coc_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id = mapped_column(Integer, ForeignKey(Customer.id), nullable=False)
    collectible_id = mapped_column(Integer, ForeignKey(Collectible.collectible_id), nullable=False)
    collectibles = relationship("Collectible", backref="Customers")
    customers = relationship("Customer", backref="Collectible")