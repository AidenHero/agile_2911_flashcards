from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from models import Customer, Flashcard, Flashcard_set
from flask_login import current_user, login_required
# from flask_login import login_user, login_required, logout_user, current_user
# from app import app

endpoint = Blueprint('pages', __name__)

def get_user_ids(current_user):
    user_set_ids = db.session.query(Flashcard_set.set_id).filter_by(customer_id = current_user.id).all()
    user_set_ids = [set_id for (set_id,) in user_set_ids]
    return user_set_ids

@endpoint.route('/')
def homepage():
    return render_template("home.html")

@endpoint.route('/login', methods=["GET"])
def login(): 
    return render_template("login.html")

@endpoint.route('/register', methods=["GET"])
def show_register_page(): 
    return render_template("register.html")

@endpoint.route('/points', methods=["GET"])
@login_required
def show_points_page(): 
    user_points = db.session.query(Customer.points).filter_by(id = current_user.id).first()
    print(user_points)
    if user_points is None:
        user_points = 0
    else:
        user_points = user_points[0]
    print(user_points)
    return render_template("points.html", user_points=user_points)

# @endpoint.route('/register', methods=["POST"]) 
# def register(): 
#     new_name = request.form['register_name']
#     new_username = request.form['register_username']
#     new_password = request.form['register_password']

#     user = Customer(name=new_name, username=new_username, password=new_password)
#     db.session.add(user)
#     db.session.commit()

#     print(new_name, new_password, new_username)
#     return render_template("register.html")