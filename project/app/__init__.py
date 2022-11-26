import logging
# from logging.config import dictConfig
from typing import Optional, Tuple

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from project.app.modules.auth.routes import router as auth
from project.app.modules.main.routes import \
    router as _main  # underscore to avoid shadowing
from project.app.modules.notificacoes.routes import router as notificacoes
from project.app.modules.ocorrencias.routes import router as ocorrencias
from project.app.modules.previsao.routes import router as previsao
from project.app.modules.uploads.routes import router as uploads
from project.app.modules.usuarios.routes import router as users

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

    

    description = """
    ChimichangApp API helps you do awesome stuff. 🚀

    ## Items

    You can **read items**.

    ## Users

    You will be able to:

    * **Create users** (_not implemented_).
    * **Read users** (_not implemented_).
    """
    # Adicionando descrição para o Swagger: https://fastapi.tiangolo.com/tutorial/metadata/
    # https://fastapi.tiangolo.com/tutorial/metadata/
    # create a new app
    app = FastAPI(middleware=middleware,
          title="ChimichangApp",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
           )


    # include external routers
    app.include_router(_main)
    app.include_router(users)
    app.include_router(auth)
    app.include_router(uploads)
    app.include_router(previsao)
    app.include_router(ocorrencias)
    app.include_router(notificacoes)

    return app, settings
