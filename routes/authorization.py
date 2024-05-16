from flask import url_for, render_template, request, Blueprint, redirect, session
from db import db
from models import Customer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


authorization_bp = Blueprint("authorization", __name__)

@authorization_bp.route('/login', methods=["POST"])
def login_auth():
    username = request.form.get("loginusername")
    password = request.form.get("loginPassword")
    user = Customer.query.filter_by(username=request.form.get("loginusername")).first()
    if user == None:
        usererror="Invalid username"
        return render_template("login.html", usererror=usererror)
    # if user.password and request.form.get("loginPassword"): 
    if check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for("pages.homepage"))
    else:
        usererror="Invalid password"
        return render_template("login.html", usererror=usererror)

    # return redirect(url_for("pages.login"))


@authorization_bp.route('/register', methods=["POST"])
def register_auth():
    if request.form.get("register_name") and request.form.get("register_username") and request.form.get("register_password"):
        existing_user = Customer.query.filter_by(username=request.form.get("register_username")).first()
        if existing_user:
            usererror = "Username already exists"
            return render_template("register.html", usererror=usererror)
        
        user=Customer(name=request.form.get("register_name"),
        username=request.form.get("register_username"),
        password = generate_password_hash(request.form.get("register_password")))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('pages.login'))
    
    usererror = "not all fields were filled"
    return render_template("register.html", usererror=usererror)

@authorization_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('pages.login'))