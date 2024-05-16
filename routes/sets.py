from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from models import Customer, Flashcard, Flashcard_set
from flask_login import current_user, login_required


sets_bp = Blueprint('sets', __name__)

@sets_bp.route('/') # display all sets
@login_required
def sets_page():
    all_sets = db.session.query(Flashcard_set).filter_by(customer_id=current_user.id).all()
    return render_template("sets.html", sets=all_sets)


@sets_bp.route('/<int:set_id>') # to display set info (for specific set_id)
@login_required
def set_detail(set_id):
    pass