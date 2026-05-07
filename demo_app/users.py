from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from .db import get_db
from .auth import require_token

bp = Blueprint("users", __name__)


@bp.route("/api/users", methods=["POST"])
def create_user():
    """Register a new user."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    firstname = data.get("firstname", "").strip()
    lastname = data.get("lastname", "").strip()
    phone = data.get("phone", "").strip()

    if not all([username, password, firstname, lastname, phone]):
        return jsonify({"error": "All fields are required"}), 400

    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (username, password, firstname, lastname, phone)"
            " VALUES (?, ?, ?, ?, ?)",
            (username, generate_password_hash(password), firstname, lastname, phone),
        )
        db.commit()
    except db.IntegrityError:
        return jsonify({"error": f"User '{username}' already exists"}), 409

    return jsonify({"message": f"User '{username}' created successfully"}), 201


@bp.route("/api/users", methods=["GET"])
def get_users():
    """Retrieve all registered users (public)."""
    db = get_db()
    users = db.execute(
        "SELECT id, username, firstname, lastname, phone FROM users"
    ).fetchall()
    return jsonify([dict(row) for row in users])


@bp.route("/api/users/<username>", methods=["GET"])
@require_token
def get_user(username):
    """Get a specific user's details (requires token)."""
    db = get_db()
    user = db.execute(
        "SELECT id, username, firstname, lastname, phone FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(dict(user))


@bp.route("/api/users/<username>", methods=["PUT"])
@require_token
def update_user(username):
    """Update a user's information (requires token)."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    db = get_db()
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if user is None:
        return jsonify({"error": "User not found"}), 404

    firstname = data.get("firstname", user["firstname"])
    lastname = data.get("lastname", user["lastname"])
    phone = data.get("phone", user["phone"])

    db.execute(
        "UPDATE users SET firstname = ?, lastname = ?, phone = ? WHERE username = ?",
        (firstname, lastname, phone, username),
    )
    db.commit()
    return jsonify({"message": f"User '{username}' updated successfully"})
