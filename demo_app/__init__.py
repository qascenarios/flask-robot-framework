import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev-secret-key",
        DATABASE=os.path.join(app.instance_path, "demo_app.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db

    db.init_app(app)
    with app.app_context():
        db.ensure_default_user()

    from . import ui

    app.register_blueprint(ui.bp)

    from . import users

    app.register_blueprint(users.bp)

    from . import auth

    app.register_blueprint(auth.bp)

    return app
