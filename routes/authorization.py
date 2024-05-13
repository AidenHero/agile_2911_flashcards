from flask import url_for, render_template, request, Blueprint, redirect, session
from db import db
from models import Customer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from models import Customer

authorization_bp = Blueprint("authorization", __name__)

@authorization_bp.route('/login', methods=["POST"])
def login():
    user = Customer.query.filter_by(
    username=request.form.get("username")).first()
    if user.password == request.form.get("password"):
        login_user(user)
        return redirect(url_for("home"))
    return render_template("login.html")


@authorization_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username=request.form.get("username")
        password=request.form.get("password")
        db.session.add()
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html")