import logging
# from logging.config import dictConfig
from typing import Optional, Tuple

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from project.app.modules.auth.routes import router as auth
from project.app.modules.instituicoes.routes import router as instituicoes
from project.app.modules.main.routes import \
    router as _main  # underscore to avoid shadowing
from project.app.modules.notificacoes.routes import router as notificacoes
from project.app.modules.ocorrencias.routes import router as ocorrencias
from project.app.modules.previsao.routes import router as previsao
from project.app.modules.tipos_ocorrencias.routes import \
    router as tipos_ocorrencias
from project.app.modules.uploads.routes import router as uploads
from project.app.modules.usuarios.routes import router as usuarios

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
    Descrição muito boa para a documentação!
    """
    # Adicionando descrição para o Swagger: https://fastapi.tiangolo.com/tutorial/metadata/
    # https://fastapi.tiangolo.com/tutorial/metadata/
    # create a new app
    app = FastAPI(middleware=middleware,
          title="Dev-Aplicado",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "aejunior",
        "url": "https://github.com/aejunior",
        "email": "user.emerson@outlook.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://github.com/matheuscarvalhodev/Dev-Aplicado-API/blob/main/LICENSE",
    },
           )


    # include external routers
    app.include_router(auth)
    app.include_router(instituicoes)
    app.include_router(_main)
    app.include_router(notificacoes)
    app.include_router(ocorrencias)
    app.include_router(previsao)
    app.include_router(tipos_ocorrencias)
    app.include_router(uploads)
    app.include_router(usuarios)

    return app, settings
