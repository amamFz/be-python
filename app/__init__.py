from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
blacklisted_tokens = set()


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    jwt = JWTManager(app)

    jwt = JWTManager(app)

    # JWT token blacklist callback
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in blacklisted_tokens

    # JWT token expired
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    # JWT invalid token
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    # JWT missing token
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    # JWT revoked token
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"message": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    db.init_app(app)

    from app.routes import blueprints

    # Perbaiki loop agar membaca (blueprint, prefix)
    for blueprint, prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=f"/api{prefix}")

    with app.app_context():
        db.create_all()

    return app
