from flask import Flask, render_template, request, Blueprint
from pathlib import Path
from db import db
from routes import endpoint, cards_bp, sets_bp, api_cards_bp, api_sets_bp

app = Flask(__name__)
bp = Blueprint("html", __name__)

app.register_blueprint(endpoint, url_prefix='/')
app.register_blueprint(cards_bp, url_prefix='/all/cards')
app.register_blueprint(sets_bp, url_prefix='/all/sets')
app.register_blueprint(api_cards_bp, url_prefix='/cards')
app.register_blueprint(api_sets_bp, url_prefix='/sets')


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.instance_path = Path("data").resolve()

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, port=8888)