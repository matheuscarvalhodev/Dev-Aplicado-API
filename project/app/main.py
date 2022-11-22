import logging

from project.app import create_app
from project.app.db import init_db

logger = logging.getLogger()

# global app
# app = None

# if __name__ == "__main__":
#     # global app
#     app, templates, config = create_app()

app, settings = create_app()


@app.on_event("startup")
async def startup() -> None:
    if settings.TESTING:  # pragma: no cover
        await init_db()