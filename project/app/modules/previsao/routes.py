from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import _TemplateResponse

from project.app.auth import hash_provider, token_provider
from project.app.db import get_session
from project.app.models import Previsao
from project.app.settings import settings

Response = _TemplateResponse | RedirectResponse

router = APIRouter(prefix="/previsao")


@router.get("", response_model=Previsao)
async def list(request: Request, session: AsyncSession = Depends(get_session)
    # , offset: int = 0, limit: int = Query(default=100, lte=100)
    ) -> Response:
    _query = select(Previsao).order_by(Previsao.id.desc()).one() #.offset(offset).limit(limit)
    _result = await session.execute(_query)
    _previsao = _result.scalars().all()
    return _previsao