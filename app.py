from flask import Flask
from pathlib import Path
from db import db
from routes import endpoint

app = Flask(__name__)
app.register_blueprint(endpoint, url_prefix='/')


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.instance_path = Path("data").resolve()

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, port=8888)