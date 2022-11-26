from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import _TemplateResponse

from project.app.auth.utils import obter_usuario_logado
from project.app.db import get_session
from project.app.models import NotificacaoResposta, Previsao, Usuario
from project.app.settings import settings

Response = _TemplateResponse | RedirectResponse

router = APIRouter(prefix="/notificacao")


@router.get("", response_model=List[NotificacaoResposta], tags=["Notificações"])
async def list(request: Request, user: Usuario=Depends(obter_usuario_logado), session: AsyncSession = Depends(get_session), 
    # sort: str = ["asc", "desc"]
    offset: int = 0, limit: int = Query(default=100, lte=100)) -> Response:
    _query = select(NotificacaoResposta).offset(offset).limit(limit).order_by(desc(NotificacaoResposta.id))
    _result = await session.execute(_query)
    _notificacao = _result.scalars().all()
    return _notificacao

@router.get("/{notificacao_id}", response_model=NotificacaoResposta, tags=["Notificações"])
async def by_id(request: Request, notificacao_id: int, user: Usuario=Depends(obter_usuario_logado), session: AsyncSession = Depends(get_session)) -> Response:
    _query = select(NotificacaoResposta).filter_by(id=notificacao_id)
    _result = await session.execute(_query)
    _notificacao: Optional[NotificacaoResposta] = _result.scalar_one_or_none()
    if not _notificacao:
        raise HTTPException(status_code=404, detail="Notificacao not found")
    return _notificacao

@router.post("/", response_model=NotificacaoResposta, tags=["Notificações"])
async def create(*, user: Usuario=Depends(obter_usuario_logado), session: AsyncSession = Depends(get_session), notificacao: NotificacaoResposta) -> Response:
    _notificacao = NotificacaoResposta(notificacao.status)
    session.add(_notificacao)
    await session.commit()
    await session.refresh(_notificacao)
    return _notificacao

@router.post("/{notificacao_id}", response_model=NotificacaoResposta, tags=["Notificações"])
async def update(notificacao_id: int, notificacao: NotificacaoResposta, user: Usuario=Depends(obter_usuario_logado), session: AsyncSession = Depends(get_session) ) -> Response:
    _query = select(NotificacaoResposta).filter_by(id=notificacao_id)
    _result = await session.execute(_query)
    _notificacao: Optional[NotificacaoResposta] = _result.scalar_one_or_none()
    if not _notificacao:
        raise HTTPException(status_code=404, detail="Notificacao not found")
    _notificacao.login = notificacao.login 
    session.add(_notificacao)
    await session.commit()
    await session.refresh(_notificacao)
    return _notificacao

@router.delete("/{notificacao_id}", tags=["Notificações"])
async def delete(notificacao_id: int, user: Usuario=Depends(obter_usuario_logado), session: AsyncSession = Depends(get_session) ) -> Response:
    _query = select(NotificacaoResposta).filter_by(id=notificacao_id)
    _result = await session.execute(_query)
    _notificacao: Optional[NotificacaoResposta] = _result.scalar_one_or_none()
    if not _notificacao:
        raise HTTPException(status_code=404, detail="Notificacao not found")
    await session.delete(_notificacao)
    await session.commit()
    return JSONResponse({"deleted": f"{notificacao_id}"})

