import os
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from .db import db
from .models.users import UserModel

ENV_TO_CONFIG = {"test": "app.configs.test.TestingConfig",
                 "dev": "app.configs.dev.DevelopmentConfig",
                 "local": "app.configs.local.LocalConfig"}


def create_app(env):
    project_root = os.path.dirname(__file__)
    template_path = os.path.join(project_root, 'templates')
    app = Flask(__name__,  template_folder=template_path)
    if env not in ENV_TO_CONFIG:
        raise ValueError("Please choose the correct environment: test/dev/local")
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
        from .controllers.conversations import conversations_blueprint

        app.register_blueprint(users_blueprint, url_prefix="/")
        app.register_blueprint(conversations_blueprint, url_prefix="/")

        db.create_all()

    return app


env = os.environ.get("ENV", "dev")
app = create_app(env)
# kwargs = {'host': '127.0.0.1', 'port': 5050, 'threaded': True, 'use_reloader': False, 'debug': False}
# flaskThread = Thread(target=app.app_context().push(), daemon=True, kwargs=kwargs).start()
app.app_context().push()