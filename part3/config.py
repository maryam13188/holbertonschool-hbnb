#!/usr/bin/python3
"""HBnB Part 3 configuration"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///hbnb_dev.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
