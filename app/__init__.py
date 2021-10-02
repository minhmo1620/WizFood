import os
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from .db import db
from .models.users import UserModel

ENV_TO_CONFIG = {"dev": "app.configs.dev.DevelopmentConfig",
                 "local": "app.configs.local.LocalConfig"}


def create_app(env):
    app = Flask(__name__)
    if env not in ENV_TO_CONFIG:
        raise ValueError("Please choose the correct environment: dev/local")
    app.config.from_object(ENV_TO_CONFIG[env])
    db.init_app(app)

    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify({"message": str(e)}), code

    with app.app_context():
        from .controllers.users import users_blueprint

        app.register_blueprint(users_blueprint, url_prefix="/")

        db.create_all()

    return app


env = os.environ.get("ENV", "development")
app = create_app(env)
app.app_context().push()
