import os
from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from .db import db

# Load the environment variable in .env
from dotenv import load_dotenv
load_dotenv()

ENV_TO_CONFIG = {"test": "app.configs.test.TestingConfig",
                 "dev": "app.configs.dev.DevelopmentConfig",
                 "local": "app.configs.local.LocalConfig",
                 "staging": "app.configs.staging.StagingConfig",
                 "production": "app.configs.production.ProductionConfig"
                 }


def create_app(env):
    project_root = os.path.dirname(__file__)
    template_path = os.path.join(project_root, 'templates')
    app = Flask(__name__,  template_folder=template_path)
    CORS(app)
    if env not in ENV_TO_CONFIG:
        raise ValueError("Please choose the correct environment: test/dev/local/staging/production")
    app.config.from_object(ENV_TO_CONFIG[env])

    # Replace the URL from postgres to postgresql+psycopg2
    uri = app.config['SQLALCHEMY_DATABASE_URI']
    if uri and uri.startswith("postgres://"):
        app.config['SQLALCHEMY_DATABASE_URI'] = uri.replace("postgres://", "postgresql+psycopg2://", 1)
    
    db.init_app(app)

    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify({"message": str(e)}), code

    with app.app_context():
        from .controllers.home import home_blueprint
        from .controllers.users import users_blueprint
        from .controllers.conversations import conversations_blueprint
        from .controllers.boxes import boxes_blueprint
        from .controllers.options import options_blueprint
        from .controllers.votes import votes_blueprint
        from .controllers.foods import foods_blueprint

        app.register_blueprint(home_blueprint, url_prefix="/")
        app.register_blueprint(users_blueprint, url_prefix="/")
        app.register_blueprint(conversations_blueprint, url_prefix="/")
        app.register_blueprint(boxes_blueprint, url_prefix="/")
        app.register_blueprint(options_blueprint, url_prefix="/")
        app.register_blueprint(votes_blueprint, url_prefix="/")
        app.register_blueprint(foods_blueprint, url_prefix="/")

        db.create_all()

    return app


env = os.environ.get("ENV", "dev")
app = create_app(env)
app.app_context().push()
