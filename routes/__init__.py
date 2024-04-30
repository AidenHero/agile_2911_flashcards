from .endpoint import endpoint

def init_app(app):
    app.register_blueprint(endpoint)