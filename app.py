from flask import Flask, render_template, request, Blueprint
from pathlib import Path
from db import db
from routes import endpoint, cards_bp, sets_bp, api_cards_bp, api_sets_bp, authorization_bp, collectibles_bp
from models import Customer
from flask_login import LoginManager

app = Flask(__name__)
bp = Blueprint("html", __name__)

app.register_blueprint(endpoint, url_prefix='/')
app.register_blueprint(cards_bp, url_prefix='/all/cards')
app.register_blueprint(sets_bp, url_prefix='/all/sets')
app.register_blueprint(api_cards_bp, url_prefix='/cards')
app.register_blueprint(api_sets_bp, url_prefix='/sets')
app.register_blueprint(authorization_bp, url_prefix='/')
app.register_blueprint(collectibles_bp, url_prefix='/collectibles')


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SECRET_KEY"] = "flashcardsharks"
app.instance_path = Path("data").resolve()
login_manager = LoginManager()
login_manager.login_view="authorization.login_auth"
login_manager.init_app(app)
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True, port=8888)