from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from models import Customer, Flashcard, Flashcard_set

cards_bp = Blueprint('cards', __name__)

@cards_bp.route('/') # display all cards
def cards_page():
    return render_template("cards.html")

@cards_bp.route('/<int:card_id>') # to display card info (for specific card_id)
def card_detail(card_id):
    card = db.get_or_404(Flashcard, card_id)
    return render_template("card_details.html", card=card)
