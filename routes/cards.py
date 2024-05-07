from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from models import Customer, Flashcard, Flashcard_set

cards_bp = Blueprint('cards', __name__)

@cards_bp.route('/') # display all cards
def cards_page():
    all_cards = db.session.execute(db.select(Flashcard)).scalars()
    return render_template("cards.html", cards=all_cards)

@cards_bp.route('/<int:card_id>') # to display card info (for specific card_id)
def card_detail(card_id):
    pass
