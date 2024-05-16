from .endpoint import endpoint
from .cards import cards_bp
from .sets import sets_bp
from .api_cards import api_cards_bp
from .api_sets import api_sets_bp
from .authorization import authorization_bp

def init_app(app):
    app.register_blueprint(endpoint)