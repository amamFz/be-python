from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity,
)
from app import blacklisted_tokens
from app.models import User
from app import db
from datetime import timedelta, datetime, timezone

auth_routes = Blueprint("auth", __name__)


@auth_routes.route("/register", methods=["POST"])
def register():
    try:
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return jsonify({"error": "Username, email, dan password harus diisi"}), 400

        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username sudah digunakan"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email sudah digunakan"}), 400

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User berhasil didaftarkan"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_routes.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email dan password harus diisi"}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({"error": "Email atau password salah"}), 400

        access_token = create_access_token(
            identity=str(user.id), expires_delta=timedelta(minutes=30)
        )
        refresh_token = create_refresh_token(identity=str(user.id))

        return (
            jsonify(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "message": "Login berhasil",
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_routes.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]
        blacklisted_tokens.add(jti)
        return jsonify({"message": "Successfully logged out"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_routes.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)

        return (
            jsonify(
                {
                    "access_token": new_access_token,
                    "message": "Token refreshed successfully",
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_routes.route("/check-token", methods=["GET"])
@jwt_required()
def check_token_status():
    """Check if the current token is valid and not expired"""
    try:
        # Get JWT claims which includes expiration
        claims = get_jwt()
        exp_timestamp = claims["exp"]

        # Get current time in UTC
        current_time = datetime.now(timezone.utc)
        current_timestamp = datetime.timestamp(current_time)

        # Calculate time remaining
        time_remaining = exp_timestamp - current_timestamp

        if time_remaining <= 0:
            return jsonify({"status": "expired", "message": "Token has expired"}), 401

        # Warning if token expires in less than 5 minutes
        if time_remaining < 300:  # 300 seconds = 5 minutes
            return (
                jsonify(
                    {
                        "status": "warning",
                        "message": "Token will expire soon",
                        "expires_in": time_remaining,
                    }
                ),
                200,
            )

        return (
            jsonify(
                {
                    "status": "valid",
                    "message": "Token is valid",
                    "expires_in": time_remaining,
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify({"status": "error", "message": f"Error checking token: {str(e)}"}),
            500,
        )
