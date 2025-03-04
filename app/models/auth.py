from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(
        db.String(255), nullable=False
    )  # Gunakan `password`, tapi simpan hash

    def set_password(self, password):
        self.password = generate_password_hash(
            password
        )  # Simpan hasil hash di `password`

    def check_password(self, password):
        return check_password_hash(
            self.password, password
        )  # Bandingkan password dengan hash

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": "[PROTECTED]",  # Jangan pernah mengembalikan password asli
        }
