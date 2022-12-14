from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.templating import _TemplateResponse

from project.app.settings import settings

# defining the response type
# this syntax is similar to the type Union
# Docs: https://peps.python.org/pep-0604/
Response = _TemplateResponse | RedirectResponse


router = APIRouter()


@router.get("/", tags=["Teste de conexão"], summary=["Realiza teste de conexão"])
async def main(request: Request) -> Response:
    return JSONResponse(content={"ping": "pong"})
