"""Flask config class."""
import os


class Config:
    """Set Flask configuration vars."""

    # General Config
    TESTING = os.environ.get('TESTING')
    DEBUG = os.environ.get('DEBUG')
    SECRET_KEY = b'M\xceid\x17\xb3\x8b\xce:{\xbf\x07v\xe2VK\x19\xdd\x00\xa1i\x13\xdbu'
    UPLOAD_FOLDER='static/pdf'
    MAX_CONTENT_LENGTH=40 * 1024 * 1024
