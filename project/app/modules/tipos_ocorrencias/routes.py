from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import _TemplateResponse

from project.app.auth.utils import obter_usuario_logado
from project.app.db import get_session
from project.app.models import TipoOcorrenciaAutuacao, Usuario
from project.app.settings import settings

Response = _TemplateResponse | RedirectResponse

router = APIRouter(prefix="/tipos-ocorrencias")


@router.get("/", response_model=List[TipoOcorrenciaAutuacao])
async def list(request: Request, user: Usuario=Depends(obter_usuario_logado), session: AsyncSession = Depends(get_session), offset: int = 0, limit: int = Query(default=100, lte=100)) -> Response:
    _query = select(TipoOcorrenciaAutuacao).offset(offset).limit(limit)
    _result = await session.execute(_query)
    _ocorrencia_autuacao = _result.scalars().all()
    return _ocorrencia_autuacao

@router.get("/{tipoOcorrenciaId}", response_model=TipoOcorrenciaAutuacao)
async def by_id(request: Request, tipoOcorrenciaId: int, user: Usuario=Depends(obter_usuario_logado), session: AsyncSession = Depends(get_session)) -> Response:
    _query = select(TipoOcorrenciaAutuacao).filter_by(id=tipoOcorrenciaId)
    _result = await session.execute(_query)
    _tipo_ocorrencia_id: Optional[TipoOcorrenciaAutuacao] = _result.scalar_one_or_none()
    if not _tipo_ocorrencia_id:
        raise HTTPException(status_code=404, detail="TipoOcorrenciaAutuacao not found")
    return _tipo_ocorrencia_id

@router.post("/", response_model=TipoOcorrenciaAutuacao)
async def create(*, user: Usuario=Depends(obter_usuario_logado), session: AsyncSession = Depends(get_session), tipo_ocorrencia: TipoOcorrenciaAutuacao) -> Response:
    _tipo_ocorrencia = TipoOcorrenciaAutuacao(
        nome= tipo_ocorrencia.nome,
        descricao= tipo_ocorrencia.descricao,
        prioridade= tipo_ocorrencia.prioridade,
        tipo= tipo_ocorrencia.tipo,
        instituicao_id= tipo_ocorrencia.instituicao_id,
        )
    session.add(_tipo_ocorrencia)
    await session.commit()
    await session.refresh(_tipo_ocorrencia)
    return _tipo_ocorrencia

@router.post("/{tipo_ocorrencia_id}", response_model=TipoOcorrenciaAutuacao)
async def update(tipo_ocorrencia_id: int, tipo_ocorrencia: TipoOcorrenciaAutuacao, user: Usuario=Depends(obter_usuario_logado), session: AsyncSession = Depends(get_session) ) -> Response:
    _query = select(TipoOcorrenciaAutuacao).filter_by(id=tipo_ocorrencia_id)
    _result = await session.execute(_query)
    _tipo_ocorrencia: Optional[TipoOcorrenciaAutuacao] = _result.scalar_one_or_none()
    
    if not _tipo_ocorrencia:
        raise HTTPException(status_code=404, detail="TipoOcorrenciaAutuacao not found")
    
    _tipo_ocorrencia.nome = tipo_ocorrencia.nome
    _tipo_ocorrencia.descricao = tipo_ocorrencia.descricao
    _tipo_ocorrencia.prioridade = tipo_ocorrencia.prioridade
    _tipo_ocorrencia.tipo = tipo_ocorrencia.tipo
    _tipo_ocorrencia.instituicao_id = tipo_ocorrencia.instituicao_id

    session.add(_tipo_ocorrencia)
    await session.commit()
    await session.refresh(_tipo_ocorrencia)
    return _tipo_ocorrencia

@router.delete("/{tipo_ocorrencia_id}")
async def delete(tipo_ocorrencia_id: int, user: Usuario=Depends(obter_usuario_logado), session: AsyncSession = Depends(get_session) ) -> Response:
    _query = select(TipoOcorrenciaAutuacao).filter_by(id=tipo_ocorrencia_id)
    _result = await session.execute(_query)
    _tipo_ocorrencia: Optional[TipoOcorrenciaAutuacao] = _result.scalar_one_or_none()
    if not _tipo_ocorrencia:
        raise HTTPException(status_code=404, detail="TipoOcorrenciaAutuacao not found")
    await session.delete(_tipo_ocorrencia)
    await session.commit()
    return JSONResponse({"message": f"{tipo_ocorrencia_id}"})

