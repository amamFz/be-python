from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import model setelah inisialisasi db untuk menghindari circular import
from .auth import User
from .models import Friend
