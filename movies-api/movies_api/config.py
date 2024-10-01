import os


class Config:
    CACHE_TYPE = "SimpleCache"
    OMDB_API_KEY = os.environ.get("OMDB_API_KEY")
    OMDB_URL = os.environ.get("OMDB_URL") or "https://www.omdbapi.com"
    JWT_SECRET_KEY = "super-secret"
    DEFAULT_USER = os.environ.get("DEFAULT_USER") or "admin"
    DEFAULT_PASSWORD = os.environ.get("DEFAULT_PASSWORD") or "admin"


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    PG_USER = os.environ.get("PG_USER")
    PG_PASSWORD = os.environ.get("PG_PASSWORD")
    PH_HOST = os.environ.get("PG_HOST")
    PG_PORT = os.environ.get("PG_PORT") or "5432"
    PG_DATABASE = os.environ.get("PG_DATABASE")
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PH_HOST}:{PG_PORT}/{PG_DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = os.environ.get("REDIS_HOST")
    CACHE_REDIS_PORT = os.environ.get("REDIS_PORT") or 6379
    CACHE_REDIS_DB = os.environ.get("REDIS_DB") or 0
    CACHE_REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
