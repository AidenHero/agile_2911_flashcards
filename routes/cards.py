from flask import Blueprint, render_template, redirect, url_for, request, stream_template
from db import db
from models import Customer, Flashcard, Flashcard_set
from flask_login import current_user,login_required

cards_bp = Blueprint('cards', __name__)

@cards_bp.route('/') # display all cards
@login_required
def cards_page():
    user_set_ids = db.session.query(Flashcard_set.set_id).filter_by(customer_id=current_user.id).all()
    user_set_ids = [set_id for (set_id,) in user_set_ids]
    user_cards = db.session.query(Flashcard).filter(Flashcard.set_id.in_(user_set_ids)).all()  
    # all_cards = db.session.execute(db.select(Flashcard)).scalars()
    return render_template("cards.html", cards=user_cards)

@cards_bp.route('/<int:card_id>') # to display card info (for specific card_id)
@login_required
def card_detail(card_id):
    card = db.get_or_404(Flashcard, card_id)
    return render_template("card_details.html", card=card)

@cards_bp.route('/answer')
@login_required
def answer_cards():
    user_set_ids = db.session.query(Flashcard_set.set_id).filter_by(customer_id=current_user.id).all()
    user_set_ids = [set_id for (set_id,) in user_set_ids]
    user_cards = db.session.query(Flashcard).filter(Flashcard.set_id.in_(user_set_ids)).all()
    # all_cards = db.session.execute(db.select(Flashcard)).scalars()
    # cards_to_answer = []
    # for card in user_cards:
    #     priority = card.priority
    #     cards_to_answer.extend(card*priority)

    # print(cards_to_answer)
    #get the sets that are being tested
    #get all the cards in that set into a list
    #get a random card, the chances of getting a card are increased depending on how prioritized that card is
    #
    return render_template("answering_cards.html", cards=user_cards, answered_card_id = 1)


@cards_bp.route('/answer/<int:set_id>')
@login_required
def answer_cards_in_set(set_id):
    user_set_ids = db.session.query(Flashcard_set.set_id).filter_by(customer_id=current_user.id).all()
    user_set_ids = [set_id for (set_id,) in user_set_ids]
    if set_id not in user_set_ids:
        return "You are not permitted to view this set."
    
    user_cards = db.session.query(Flashcard).filter_by(set_id = set_id).all()
    return render_template("answering_cards.html", cards=user_cards, answered_card_id = 1)

@cards_bp.route("/answer", methods=["POST"])
@login_required
def to_answer():
    # user_set_ids = db.session.query(Flashcard_set.set_id).filter_by(customer_id=current_user.id).all()
    # user_set_ids = [set_id for (set_id,) in user_set_ids]
    # user_cards = db.session.query(Flashcard).filter(Flashcard.set_id.in_(user_set_ids)).all()
    
    all_cards = db.session.execute(db.select(Flashcard)).scalars()

    key = list(request.form.keys())[0]
    value = request.form[key]
    intkey = int(key)
    card = db.get_or_404(Flashcard, intkey)
    if value == card.answer:
        outcome = "correct"
    else:
        outcome = "wrong"
    print(card.flash_id)
    return stream_template("answering_cards.html", cards=all_cards, answered_card_id = card.flash_id, answer = outcome)