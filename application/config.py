import os
from pathlib import Path

TOP_DIR = Path(__file__)


class Config:
    DEBUG = False
    TESTING = False

    FLASK_ADMIN_SWATCH = 'cyborg'


class ProductionConfig(Config):
    pass


class TestConfig(Config):

    # set debug and testing to true
    DEBUG = True
    TESTING = True

    # get test database default
    db_dir = TOP_DIR.parent / '..' / 'tests' / 'database'
    db_dir.mkdir(parents=True, exist_ok=True)
    db_path = str(db_dir / 'test.db')

    # Secret key for flask app
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fake-news')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{db_path}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
