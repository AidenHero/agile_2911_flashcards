from flask import Blueprint, render_template, redirect, url_for, request, stream_template, flash
from db import db
from models import Customer, Flashcard, Flashcard_set, Collectible, Customer_Owned_Collectible
from flask_login import current_user,login_required
from random import randint
collectibles_bp = Blueprint('collectibles', __name__)


@collectibles_bp.route("/buy")
@login_required
def buy_collectible():
    user = db.get_or_404(Customer, current_user.id)
    if user.points < 100:
        message="Not enough points to get a collectible"
        return render_template("collectible_response.html", message=message)
    
    user.points -= 100
    db.session.commit()
    collectibles = db.session.query(Collectible)
    collectibles = [collectible for (collectible) in collectibles]
    
    x = randint(1,len(collectibles))
    owned_collectibles = user.Collectible
    owned_collectibles = [collectible_id.collectible_id for collectible_id in owned_collectibles]
    if x in owned_collectibles:
        message="Unlucky, you already own that collectible"
        return render_template("collectible_response.html", message=message)
    
    db.session.add(Customer_Owned_Collectible(customer_id = current_user.id, collectible_id = x))
    message="Congrats, you got a new collectible!"
    db.session.commit()
    return render_template("collectible_response.html", message=message)

@collectibles_bp.route("/collectibles")
@login_required
def view_collectibles():
    user = db.get_or_404(Customer, current_user.id)
    owned_collectibles = db.session.query(Customer_Owned_Collectible).filter_by(customer_id=user.id).all()
    return render_template("collectibles.html", collectibles=owned_collectibles)
