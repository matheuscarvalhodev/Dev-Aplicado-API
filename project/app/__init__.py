import logging

# from logging.config import dictConfig
from typing import Optional, Tuple

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from project.app.modules.main.routes import (
    router as _main,  # underscore to avoid shadowing
)

from .settings import BaseSettings, get_settings

logger = logging.getLogger()


def create_app(
    app_settings: Optional[str] = None,
) -> Tuple[FastAPI, BaseSettings]:
    settings = get_settings(app_settings)

    # configuring the logging
    # for more info, check:
    # https://docs.python.org/3.10/howto/logging.html
    # this configuration writes to a file and to the console
    # dictConfig(
    #     {
    #         "version": 1,
    #         "formatters": {
    #             "default": {
    #                 "format": "[%(asctime)s] [%(levelname)s] [%(name)s] "
    #                 "[%(module)s:%(lineno)s] - %(message)s",
    #             }
    #         },
    #         "handlers": {
    #             "console": {
    #                 "class": "logging.StreamHandler",
    #                 "formatter": "default",
    #             },
    #             # "to_file": {
    #             #     "level": "DEBUG",
    #             #     "formatter": "default",
    #             #     "class": "logging.handlers.RotatingFileHandler",
    #             #     "filename": "logs/messages.log",
    #             #     "maxBytes": 5000000,
    #             #     "backupCount": 10,
    #             # },
    #         },
    #         "root": {
    #             "level": config.LOG_LEVEL,
    #             # "handlers": ["console", "to_file"],
    #             "handlers": ["console"],
    #         },
    #     }
    # )

    # set middleware
    middleware = [Middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)]

    # create a new app
    app = FastAPI(middleware=middleware)

    # mounting static files
    app.mount("/static", StaticFiles(directory="project/app/static"), name="static")

    # include external routers
    app.include_router(_main)

    return app, settings
