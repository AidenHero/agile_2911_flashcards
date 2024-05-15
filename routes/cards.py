from flask import Blueprint, render_template, redirect, url_for, request, stream_template
from db import db
from models import Customer, Flashcard, Flashcard_set

cards_bp = Blueprint('cards', __name__)

@cards_bp.route('/') # display all cards
def cards_page():

    all_cards = db.session.execute(db.select(Flashcard)).scalars()
    return render_template("cards.html", cards=all_cards)

@cards_bp.route('/<int:card_id>') # to display card info (for specific card_id)
def card_detail(card_id):
    card = db.get_or_404(Flashcard, card_id)
    return render_template("card_details.html", card=card)

@cards_bp.route('/answer')
def answer_cards():
    all_cards = db.session.execute(db.select(Flashcard)).scalars()
    return render_template("answering_cards.html", cards=all_cards, answered_card_id = 1)

@cards_bp.route("/answer", methods=["POST"])
def to_answer():
    all_cards = db.session.execute(db.select(Flashcard)).scalars()

    key = list(request.form.keys())[0]
    value = request.form[key]
    intkey = int(key)
    card = db.get_or_404(Flashcard, intkey)
    if value == card.answer:
        outcome = "correct"
    else:
        outcome = "wrong"
    return stream_template("answering_cards.html", cards=all_cards, answered_card_id = card.flash_id, answer = outcome)