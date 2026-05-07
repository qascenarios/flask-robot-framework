import secrets
from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from .db import get_db

bp = Blueprint("auth", __name__)


def require_token(f):
    """Decorator to protect API routes with token authentication."""
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Token")
        if not token:
            return jsonify({"error": "Token required"}), 401
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE token = ?", (token,)).fetchone()
        if user is None:
            return jsonify({"error": "Invalid token"}), 401
        request.current_user = user
        return f(*args, **kwargs)

    return decorated


@bp.route("/api/auth/token", methods=["GET"])
def get_token():
    """Generate an auth token via HTTP Basic Auth."""
    auth = request.authorization
    if not auth:
        return jsonify({"error": "Authorization required"}), 401

    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE username = ?", (auth.username,)
    ).fetchone()

    if user is None or not check_password_hash(user["password"], auth.password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = secrets.token_hex(32)
    db.execute("UPDATE users SET token = ? WHERE id = ?", (token, user["id"]))
    db.commit()

    return jsonify({"token": token})
