from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db

bp = Blueprint("ui", __name__)


@bp.route("/")
def index():
    user = None
    if "user_id" in session:
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE id = ?", (session["user_id"],)
        ).fetchone()
    return render_template("index.html", user=user)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        firstname = request.form.get("firstname", "").strip()
        lastname = request.form.get("lastname", "").strip()
        phone = request.form.get("phone", "").strip()

        error = None
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif not firstname:
            error = "First name is required."
        elif not lastname:
            error = "Last name is required."
        elif not phone:
            error = "Phone number is required."

        if error is None:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO users (username, password, firstname, lastname, phone)"
                    " VALUES (?, ?, ?, ?, ?)",
                    (
                        username,
                        generate_password_hash(password),
                        firstname,
                        lastname,
                        phone,
                    ),
                )
                db.commit()
                return redirect(url_for("ui.login"))
            except Exception:
                error = f"User '{username}' is already registered."

        flash(error)

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        error = None
        if user is None or not check_password_hash(user["password"], password):
            error = "Invalid username or password."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("ui.user_info"))

        flash(error)

    return render_template("login.html")


@bp.route("/user-info")
def user_info():
    if "user_id" not in session:
        return redirect(url_for("ui.login"))
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE id = ?", (session["user_id"],)
    ).fetchone()
    return render_template("user_info.html", user=user)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("ui.index"))
