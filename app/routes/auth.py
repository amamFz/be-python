from flask import Blueprint, request, jsonify
from app.models import User
from app import db

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

        return jsonify({"message": "Login berhasil"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
