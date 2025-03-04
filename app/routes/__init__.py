from flask import Blueprint

from .friend import friend_routes
from .auth import auth_routes

blueprints = [
    (friend_routes, "/friends"),
    (auth_routes, "/auth"),
]  # Simpan dalam bentuk tuple (blueprint, prefix)
