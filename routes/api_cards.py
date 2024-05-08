from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from models import Customer, Flashcard, Flashcard_set
from sqlalchemy.sql import func
api_cards_bp = Blueprint('api_cards', __name__)

@api_cards_bp.route('/', methods=["GET"])
def make_card_screen():
    setIds = db.session.execute(db.select(Flashcard_set.set_id).order_by(Flashcard_set.set_id)).scalars()
    print(setIds)
    return render_template("create_card.html", sets=setIds)


@api_cards_bp.route('/', methods=["POST"]) # to make new card
def post_card():
    setIds = db.session.execute(db.select(Flashcard_set.set_id).order_by(Flashcard_set.set_id)).scalars()
    addquestion = request.form['card_question']
    addanswer = request.form['card_answer']
    cardset = request.form['card_set']

    card = Flashcard(question=addquestion, answer = addanswer, set_id = cardset, time_created = func.now())
    db.session.add(card)
    db.session.commit()
    print(addquestion, addanswer, cardset)
    return render_template("create_card.html", sets=setIds)

@api_cards_bp.route('/<int:card_id>', methods=["PUT"]) # to update a card (using card_id)
def put_card(card_id):
    pass

@api_cards_bp.route("/<int:card_id>/delete", methods=["POST"]) # to delete a card (using HTML)
def delete_card(card_id):
    card = db.get_or_404(Flashcard_set, card_id) # it either gets the Order instance from the databse, or returns 404 for not found 

    if card is None: # if there's no customer with that ID, return error
        return "Card not found", 404
    else: 
        product_orders = ProductOrder.query.filter_by(order_id=order_id).all()
        if product_orders is not None: 
            for each in product_orders:
                if each.order.processed is None: # check that it's not processed already before allowing to delete 
                    db.session.delete(each)
                else: 
                    return "Order already processed. Cannot delete.", 404
                
        # Delete the order
        db.session.delete(order)
        db.session.commit()
        return redirect(url_for("orders.order"))
