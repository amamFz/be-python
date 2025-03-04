from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import blueprints

    # Perbaiki loop agar membaca (blueprint, prefix)
    for blueprint, prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=f"/api{prefix}")

    with app.app_context():
        db.create_all()

    return app
