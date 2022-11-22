from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.templating import _TemplateResponse

from project.app.settings import settings

# defining the response type
# this syntax is similar to the type Union
# Docs: https://peps.python.org/pep-0604/
Response = _TemplateResponse | RedirectResponse


router = APIRouter(prefix="/usuarios")

logger = logging.getLogger()


@router.get("/")
async def main(request: Request) -> Response:
    return JSONResponse(content={"hello": "world"})
