from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from models import Customer, Flashcard, Flashcard_set

sets_bp = Blueprint('sets', __name__)

@sets_bp.route('/') # display all sets
def sets_page():
    all_sets = db.session.execute(db.select(Flashcard_set)).scalars()
    return render_template("sets.html", sets=all_sets)


# @sets_bp.route('/<int:set_id>') # to display set info (for specific set_id)
# def set_detail(set_id):
#     pass