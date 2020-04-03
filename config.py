"""Flask config class."""
import os


class Config_app:
    """Set Flask configuration vars."""

    # General Config
    TESTING = True
    DEBUG = True
    SECRET_KEY = b'M\xceid\x17\xb3\x8b\xce:{\xbf\x07v\xe2VK\x19\xdd\x00\xa1i\x13\xdbu'
    UPLOAD_FOLDER='static/pdf'
    MAX_CONTENT_LENGTH=40 * 1024 * 1024
