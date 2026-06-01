import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD_RAW = os.getenv("DB_PASSWORD")
    if not DB_PASSWORD_RAW or DB_PASSWORD_RAW == "CHANGE_THIS_TO_YOUR_MYSQL_PASSWORD":
        raise RuntimeError(
            "DB_PASSWORD is missing or still set to the placeholder. Open .env and replace "
            "CHANGE_THIS_TO_YOUR_MYSQL_PASSWORD with the MySQL root password you created."
        )
    DB_PASSWORD = quote_plus(DB_PASSWORD_RAW)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "net_banking")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
