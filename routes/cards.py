from flask import Blueprint, render_template, redirect, url_for, request, stream_template
from db import db
from models import Customer, Flashcard, Flashcard_set
from flask_login import current_user,login_required
from random import randint
cards_bp = Blueprint('cards', __name__)

def get_user_ids(current_user):
    user_set_ids = db.session.query(Flashcard_set.set_id).filter_by(customer_id = current_user.id).all()
    user_set_ids = [set_id for (set_id,) in user_set_ids]
    return user_set_ids

@cards_bp.route('/') # display all cards
@login_required
def cards_page():
    user_set_ids = get_user_ids(current_user)
    user_cards = db.session.query(Flashcard).filter(Flashcard.set_id.in_(user_set_ids)).all()  
    # all_cards = db.session.execute(db.select(Flashcard)).scalars()
    return render_template("cards.html", cards=user_cards)

@cards_bp.route('/<int:card_id>') # to display card info (for specific card_id)
@login_required
def card_detail(card_id):
    card = db.get_or_404(Flashcard, card_id)
    return render_template("card_details.html", card=card)

# @cards_bp.route('/answer')
# @login_required
# def answer_cards():
#     user_set_ids = db.session.query(Flashcard_set.set_id).filter_by(customer_id=current_user.id).all()
#     user_set_ids = [set_id for (set_id,) in user_set_ids]
#     user_cards = db.session.query(Flashcard).filter(Flashcard.set_id.in_(user_set_ids)).all()
#     # all_cards = db.session.execute(db.select(Flashcard)).scalars()
#     # cards_to_answer = []
#     # for card in user_cards:
#     #     priority = card.priority
#     #     cards_to_answer.extend(card*priority)

#     # print(cards_to_answer)
#     #get the sets that are being tested
#     #get all the cards in that set into a list
#     #get a random card, the chances of getting a card are increased depending on how prioritized that card is
#     #
#     return render_template("answering_cards.html", cards=user_cards, answered_card_id = 1)

@cards_bp.route('/answer/<int:set_id>')
@login_required
def answer_cards_in_set(set_id):
    user_set_ids = get_user_ids(current_user)

    if set_id not in user_set_ids: #in case someone types in the set id
        return "You are not permitted to view this set."
    
    user_cards = db.session.query(Flashcard.flash_id).filter_by(set_id = set_id).all()
    card_ids = db.session.query(Flashcard.flash_id).filter_by(set_id = set_id).all()

    card_ids = [card_id for (card_id,) in user_cards]
    prio_cards = []# a list of all cards, with cards with higher priority more likely to be chosen because they occur more often in the list
    for card_id in card_ids:
        card = db.get_or_404(Flashcard, card_id)
        # card.priority = randint(1,4) ** for testing purposes only
        priority = card.priority 
        prio_cards.extend([card_id] *int(priority)) # puts the card into the list a numhber of times equal to priority. ie card 5 with priority 2 would look like [card5, card5]
    
    cardID = prio_cards[randint(0,len(prio_cards)-1)] #randomly gets one of the cards
    card = db.get_or_404(Flashcard, cardID)
    return render_template("answer_cards.html", card=card, set_id = set_id) 


@cards_bp.route('/quiz/<int:set_id>')
@login_required
def quiz_cards_in_set(set_id):
    user_set_ids = get_user_ids(current_user)

    if set_id not in user_set_ids:
        return "You are not permitted to view this set."
    
    user_cards = db.session.query(Flashcard).filter_by(set_id = set_id).all()
    return render_template("quiz_cards.html", cards=user_cards, start_card_index = 1)

@cards_bp.route("/answer/<int:set_id>", methods=["POST"])
@login_required
def to_answer(set_id):
    user_set_ids = get_user_ids(current_user)

    if set_id not in user_set_ids:
        return "You are not permitted to view this set."
    key = list(request.form.keys())[0]
    value = request.form[key]
    intkey = int(key)
    card = db.get_or_404(Flashcard, intkey)
    user = db.get_or_404(Customer, current_user.id)
    if value.lower() == card.answer.lower():
        outcome = "correct"
        card.priority -=1
        user.points += 10
        if card.priority <= 0:
            card.priority = 1
        
    else:
        outcome = "wrong"
        card.priority += 1
        if card.priority >= 6:
            card.priority = 5

        
    db.session.commit()

    return render_template("answer_cards.html", card = card, answer = outcome, answered_card_id = card.flash_id, set_id = set_id)