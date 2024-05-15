from flask import url_for, render_template, request, Blueprint, redirect, session
from db import db
from models import Customer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

authorization_bp = Blueprint("authorization", __name__)

@authorization_bp.route('/login', methods=["POST"])
def login_auth():
    user = db.session.query(Customer).filter_by(username=request.form["loginusername"]).first()
    print(user)
    # if user.password and request.form.get("loginPassword"): 
    if user.password == request.form.get("loginPassword"):
        login_user(user)
        return redirect(url_for("pages.homepage"))
    return redirect(url_for("pages.login"))


@authorization_bp.route('/register', methods=["POST"])
def register_auth():
    if request.form.get("register_name") and request.form.get("register_username") and request.form.get("register_password"):
        user=Customer(name=request.form.get("register_name"),
        username=request.form.get("register_username"),
        password=request.form.get("register_password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('pages.login'))
    return render_template("pages.show_register_page")