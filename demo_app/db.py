import sqlite3
import click
from flask import current_app, g
from werkzeug.security import generate_password_hash


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))
    ensure_default_user()


def ensure_default_user():
    db = get_db()
    try:
        existing = db.execute(
            "SELECT id FROM users WHERE username = ?", ("tester2022",)
        ).fetchone()
    except sqlite3.OperationalError:
        return

    if existing is None:
        db.execute(
            "INSERT INTO users (username, password, firstname, lastname, phone) VALUES (?, ?, ?, ?, ?)",
            (
                "tester2022",
                generate_password_hash("Tester@@4040"),
                "Test",
                "User",
                "000000000",
            ),
        )
        db.commit()


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
