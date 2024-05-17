from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from models import Customer, Flashcard, Flashcard_set
from flask_login import current_user, login_required


api_sets_bp = Blueprint('api_sets', __name__)

@api_sets_bp.route('/create', methods=["GET"]) # view create set page
@login_required
def make_set_screen():
    return render_template("create_set.html")


# # !! NOT FINISHED YET !! needs dynamic customer_id
@api_sets_bp.route('/create', methods=["POST"]) # to make new set
@login_required
def post_set():
    new_set_name = request.form['set_name']
    new_set_descript = request.form['set_descript']

    set = Flashcard_set(name=new_set_name, description=new_set_descript, customer_id=current_user.id)
    db.session.add(set)
    db.session.commit()
    print(new_set_name, new_set_descript)
    return render_template("create_set.html")


@api_sets_bp.route('/<int:set_id>/update', methods=["GET"]) # view update screen
@login_required
def view_update_set(set_id):
    specific_set = db.session.execute(db.select(Flashcard_set).where(Flashcard_set.set_id == set_id)).scalar()
    if specific_set is None or specific_set.customer_id != current_user.id:
        return "Set not found or access denied", 404
    return render_template("update_set.html", set = specific_set)

@api_sets_bp.route('/<int:set_id>/update', methods=["POST"]) # to update a set (using HTML)
@login_required
def put_set(set_id):
    updated_name = request.form['updated_name']
    updated_descrp = request.form['updated_descrp']

    set = db.get_or_404(Flashcard_set, set_id)
    if set.customer_id != current_user.id:
        return "Access denied", 403
    
    if updated_name == "":
        new_name = set.name
    else: 
        new_name = updated_name

    if updated_descrp == "": 
        new_descrip = set.description
    else:
        new_descrip = updated_descrp
        
    set.name = new_name
    set.description = new_descrip
    db.session.commit()
    return redirect(url_for("sets.sets_page"))


@api_sets_bp.route('/<int:set_id>/delete', methods=["POST"]) # to delete a set (using HTML)
@login_required
def delete_set(set_id):
    set = db.get_or_404(Flashcard_set, set_id) # it either gets the Flashcard_set instance from the databse, or returns 404 for not found 

    if set.customer_id != current_user.id:
        return "Access denied", 403
    if set is None: # if there's no set with that ID, return error
        return "Set not found", 404
    else:                 
        # Delete the order
        db.session.delete(set)
        db.session.commit()
        return redirect(url_for("sets.sets_page"))
