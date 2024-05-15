from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from models import Customer, Flashcard, Flashcard_set
from sqlalchemy.sql import func
api_cards_bp = Blueprint('api_cards', __name__)

@api_cards_bp.route('/', methods=["GET"])
def make_card_screen():
    setIds = db.session.execute(db.select(Flashcard_set).order_by(Flashcard_set.set_id)).scalars()
    print(setIds)
    return render_template("create_card.html", sets=setIds)


@api_cards_bp.route('/', methods=["POST"]) # to make new card
def post_card():
    setIds = db.session.execute(db.select(Flashcard_set.set_id).order_by(Flashcard_set.set_id)).scalars()

    req_values = ['card_question', 'card_answer', 'card_set']

    for value in req_values:
        if value not in request.form:
            return f"Missing data: {value}", 400
    addquestion = request.form['card_question']
    addanswer = request.form['card_answer']
    cardset = request.form['card_set']

    card = Flashcard(question=addquestion, answer = addanswer, set_id = cardset, time_created = func.now())
    db.session.add(card)
    db.session.commit()
    print(addquestion, addanswer, cardset)
    # return render_template("create_card.html", sets=setIds)
    return redirect(url_for('cards.cards_page'))


@api_cards_bp.route('/<int:card_id>/update', methods=["POST"]) # to update a card (using card_id)
def put_card(card_id):
    updateinfo = request.form
    card = db.get_or_404(Flashcard, card_id)
    if updateinfo["new_answer"] == "":
        new_answer = card.answer
    else: 
        new_answer = updateinfo["new_answer"]

    if updateinfo["new_question"] == "": 
        new_question = card.question
    else:
        new_question = updateinfo["new_question"]
        
    card.question = new_question
    card.answer = new_answer
    db.session.commit()
    return redirect(url_for('cards.cards_page')), 302

    # return [new_question, new_answer]

@api_cards_bp.route('/<int:card_id>/delete', methods=["POST"]) # to delete a card (using HTML)
def delete_card(card_id):
    card = db.get_or_404(Flashcard, card_id)
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('cards.cards_page'))
    # return "You deleted that card"