import os
from pathlib import Path

from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from werkzeug.utils import import_string

# Possible configurations
# TODO: Make production the default at some point
config_dict = {
    "production": "application.config.ProductionConfig",
    "testing": "application.config.TestConfig",
    "default": "application.config.TestConfig",
}

# Database index naming conventions
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

# Set globals
admininstrator = Admin(name="Betfund")
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()


def create_app(test_config=True):
    """
    Initialize the application.
    """
    app = Flask(__name__, instance_relative_config=False)

    # Get the appropriate configuration, and instantiate it
    config_name = os.getenv("FLASK_CONFIGURATION", "default")
    config = import_string(config_dict[config_name])()
    app.config.from_object(config)

    ## Initialize plug-ins

    # `flask-admin`
    admininstrator.init_app(app)

    # `flask-sqlalchemy`
    db.init_app(app)
    db.app = app

    # `flask-login`
    login_manager.init_app(app)

    # `flask-mail`
    mail.init_app(app)

    # `flask-migrate`
    # TODO: `render_as_batch` only for SQLite..
    migrate.init_app(app, db, render_as_batch=True)

    with app.app_context():

        ## Register the the Blueprints
        # Home page
        from application.views.home import home_bp
        app.register_blueprint(home_bp, url_prefix="/")

        # Login page
        from application.views.auth import login_bp
        app.register_blueprint(login_bp)

        # Signup page
        from application.views.auth import signup_bp
        app.register_blueprint(signup_bp)

        # Dashboard page
        from application.views.dashboard import dashboard_bp
        app.register_blueprint(dashboard_bp)

        # Funds page
        from application.views.funds import funds_bp
        app.register_blueprint(funds_bp)

        # Transactions page
        from application.views.transactions import transactions_bp
        app.register_blueprint(transactions_bp)

        # Import the Admin views
        from application.views.admin import add_admin_views
        add_admin_views(admininstrator)

    return app
