from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from models import Customer, Flashcard, Flashcard_set

endpoint = Blueprint('pages', __name__)

@endpoint.route('/')
def homepage():
    return render_template("home.html")

@endpoint.route('/login', methods=["GET"])
def login(): 
    return render_template("login.html")

@endpoint.route('/register', methods=["GET"])
def show_register_page(): 
    return render_template("register.html")


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