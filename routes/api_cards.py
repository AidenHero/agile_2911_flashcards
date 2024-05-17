from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from models import Customer, Flashcard, Flashcard_set
from sqlalchemy.sql import func
from flask_login import current_user, login_required

api_cards_bp = Blueprint('api_cards', __name__)


@api_cards_bp.route('/', methods=["GET"])
@login_required
def make_card_screen():
    user_set_ids = db.session.query(Flashcard_set.set_id).filter_by(customer_id=current_user.id).all()
    user_set_ids = [set_id for (set_id,) in user_set_ids]
    user_sets = db.session.query(Flashcard_set).filter(Flashcard_set.set_id.in_(user_set_ids)).all()
    # setIds = db.session.execute(db.select(Flashcard_set).order_by(Flashcard_set.set_id)).scalars()
    # print(setIds)
    return render_template("create_card.html", sets=user_sets), 200


@api_cards_bp.route('/', methods=["POST"]) # to make new card
@login_required
def post_card():
    setIds = db.session.execute(db.select(Flashcard_set.set_id).order_by(Flashcard_set.set_id)).scalars()
    necessary_values = ['card_question', 'card_answer', 'card_set']
    for value in necessary_values:
        if value not in request.form:
            return "ERR: INVALID ARGS", 400
    try:
        int(request.form[necessary_values[2]])
    except:
        return "ERR: INVALID SET DATA", 400

    addquestion = request.form[necessary_values[0]]
    addanswer = request.form[necessary_values[1]]
    cardset = request.form[necessary_values[2]]
    
    db.get_or_404(Flashcard_set, cardset)
    card = Flashcard(question=addquestion, answer = addanswer, set_id = cardset, time_created = func.now())
    db.session.add(card)
    db.session.commit()
    # print(addquestion, addanswer, cardset)
    # return render_template("create_card.html", sets=setIds)
    return redirect(url_for('cards.cards_page'), 302)


@api_cards_bp.route('/<int:card_id>/update', methods=["POST"]) # to update a card (using card_id)
@login_required
def put_card(card_id):
    updateinfo = request.form
    card = db.get_or_404(Flashcard, card_id)
    if "new_answer" not in updateinfo or updateinfo["new_answer"] == "":
        new_answer = card.answer
    else: 
        new_answer = updateinfo["new_answer"]

    if "new_question" not in updateinfo or updateinfo["new_question"] == "": 
        new_question = card.question
    else:
        new_question = updateinfo["new_question"]
        
    card.question = new_question
    card.answer = new_answer
    db.session.commit()
    return redirect(url_for('cards.cards_page'),302)

    # return [new_question, new_answer]

@api_cards_bp.route('/<int:card_id>/delete', methods=["POST"]) # to delete a card (using HTML)
@login_required
def delete_card(card_id):
    card = db.get_or_404(Flashcard, card_id)
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('cards.cards_page'),302)
    # return "You deleted that card"