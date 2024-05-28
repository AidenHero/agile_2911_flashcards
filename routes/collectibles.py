from flask import Blueprint, render_template, redirect, url_for, request, stream_template
from db import db
from models import Customer, Flashcard, Flashcard_set, Collectible, Customer_Owned_Collectible
from flask_login import current_user,login_required
from random import randint
collectibles_bp = Blueprint('collectibles', __name__)

def view_collectibles():
    pass

@collectibles_bp.route("/buy")
@login_required
def buy_collectible():
    user = db.get_or_404(Customer, current_user.id)
    if user.points < 100:
        return "Not enough points to get a collectible"
    
    user.points -= 100
    collectibles = db.session.query(Collectible)
    collectibles = [collectible for (collectible) in collectibles]
    print(collectibles)
    x = randint(1, len(collectibles))
    owned_collectibles = user.Collectible
    owned_collectibles = [collectible_id.collectible_id for collectible_id in owned_collectibles]
    if x in owned_collectibles:
        return "Unlucky, you already own that collectible"
    
    db.session.add(Customer_Owned_Collectible(customer_id = current_user.id, collectible_id = x))
    return "Coongratts, you got a new collectible!"

