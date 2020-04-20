"""Flask config class."""
import os


class Config:
    """Set Flask configuration vars."""

    # General Config
    TESTING = os.environ.get('TESTING')
    DEBUG = os.environ.get('DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER='static/pdf'
    MAX_CONTENT_LENGTH=40 * 1024 * 1024
