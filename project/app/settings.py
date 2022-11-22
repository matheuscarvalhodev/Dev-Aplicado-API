import importlib
import os
from typing import Optional

from fastapi.templating import Jinja2Templates



class BaseSettings:
    TESTING = False
    SECRET_KEY = ">s&}24@{]]#k3&^5$f3#aef37959c3174caf04f766a47758e2f6"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    REDIS_URL = "redis://redis-db:6379"
    JINJA_AUTO_RELOAD = True
    LOG_LEVEL = "DEBUG"
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_ECHO = True
    templates: Jinja2Templates = None  # type: ignore


class DevelopmentSettings(BaseSettings):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or ""
    # REDIS_URL = os.environ.get("REDIS_URL") or ""
    SQLALCHEMY_ECHO = True


class TestingSettings(BaseSettings):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///./test_db.db"
    SESSION_TYPE = "filesystem"
    SQLALCHEMY_ECHO = True


class ProductionSettings(BaseSettings):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or ""
    SQLALCHEMY_ECHO = False
    JINJA_AUTO_RELOAD = False
    LOG_LEVEL = "INFO"


global settings  # pylint: disable=global-at-module-level
settings: BaseSettings = None  # type: ignore


def get_settings(app_settings: Optional[str] = None) -> BaseSettings:
    global settings  # pylint: disable=global-statement
    if settings is None:
        module = importlib.import_module("project.app.settings", package="project")
        if app_settings is not None:
            # loading the configuration
            class_ = getattr(module, app_settings)
            settings = class_()
        else:
            # loading the configuration
            _app_settings = os.getenv("APP_SETTINGS", "DevelopmentSettings")
            class_ = getattr(module, _app_settings)

        settings = class_()


    return settings


settings = get_settings()
