import os
from pathlib import Path

from flask import Flask
from werkzeug.utils import import_string

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Possible configurations
# TODO :: Make production the default at some point
config_dict = {
    "production": "application.config.ProductionConfig",
    "testing": "application.config.TestConfig",
    "default": "application.config.TestConfig"
}

# Set globals
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(test_config=True):
    """
    Initialize the application.
    """
    app = Flask(__name__, instance_relative_config=False)

    # Get the appropriate configuration, and instantiate it
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    config = import_string(config_dict[config_name])()
    app.config.from_object(config)

    # Initialize plug-ins
    db.init_app(app)
    db.app = app
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():

        # Import the the Blueprints
        # (this has to happen inside the app context)
        from application.home.home_routes import home_bp
        from application.loggedin.loggedin_routes import loggedin_bp
        from application.signup.signup_routes import signup_bp
        from application.login.login_routes import login_bp
        from application.admin.admin_routes import admin_bp

        # Register Blueprints
        app.register_blueprint(home_bp, url_prefix='/')
        app.register_blueprint(loggedin_bp)
        app.register_blueprint(signup_bp)
        app.register_blueprint(login_bp)
        app.register_blueprint(admin_bp)

        return app
