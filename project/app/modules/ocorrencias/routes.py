from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import _TemplateResponse

from project.app.auth.utils import obter_usuario_logado
from project.app.db import get_session
from project.app.models import Ocorrencia, OcorrenciaCreate, Usuario
from project.app.settings import settings

Response = _TemplateResponse | RedirectResponse

router = APIRouter(prefix="/ocorrencias")


@router.get("", response_model=List[Ocorrencia], tags=["Ocorrências"], summary=["Lista todas as ocorrências"])
async def list(request: Request, user: Usuario=Depends(obter_usuario_logado), session: AsyncSession = Depends(get_session), offset: int = 0, limit: int = Query(default=100, lte=100)) -> Response:
    _query = select(Ocorrencia).offset(offset).limit(limit)
    _result = await session.execute(_query)
    _ocorrencias = _result.scalars().all()
    return _ocorrencias

@router.get("/{ocorrencia_id}", response_model=Ocorrencia, tags=["Ocorrências"], summary=["Lista ocorrência a partir do id"])
async def by_id(request: Request, ocorrencia_id: int, user: Usuario=Depends(obter_usuario_logado), session: AsyncSession = Depends(get_session)) -> Response:
    _query = select(Ocorrencia).filter_by(id=ocorrencia_id)
    _result = await session.execute(_query)
    _ocorrencia: Optional[Ocorrencia] = _result.scalar_one_or_none()
    if not _ocorrencia:
        raise HTTPException(status_code=404, detail="Ocorrencia not found")
    return _ocorrencia

@router.post("/", response_model=Ocorrencia, tags=["Ocorrências"], summary=["Criar nova ocorrência"])
async def create(*, 
    session: AsyncSession = Depends(get_session),
    user: Usuario=Depends(obter_usuario_logado), 
    ocorrencia: OcorrenciaCreate) -> Response:
    _ocorrencia = Ocorrencia(
        address= ocorrencia.address,
        name= ocorrencia.name,
        tel= ocorrencia.tel,
        agente_id= ocorrencia.agente_id,
        alerta_id= ocorrencia.alerta_id,
        instituicao_id= ocorrencia.instituicao_id,
        long= ocorrencia.long,
        lati= ocorrencia.lati,
        usuario_id= ocorrencia.usuario_id,
        )
    session.add(_ocorrencia)
    await session.commit()
    await session.refresh(_ocorrencia)
    return _ocorrencia

@router.post("/{ocorrencia_id}", response_model=Ocorrencia, tags=["Ocorrências"], summary=["Atualiza informações da ocorrência"])
async def update(
    ocorrencia_id: int, 
    ocorrencia: Ocorrencia,
    user: Usuario=Depends(obter_usuario_logado), 
    session: AsyncSession = Depends(get_session) 
    ) -> Response:
    _query = select(Ocorrencia).filter_by(id=ocorrencia_id)
    _result = await session.execute(_query)
    _ocorrencia: Optional[Ocorrencia] = _result.scalar_one_or_none()
    if not _ocorrencia:
        raise HTTPException(status_code=404, detail="Ocorrencia not found")
    _ocorrencia.address = ocorrencia.address
    _ocorrencia.name = ocorrencia.name
    _ocorrencia.tel = ocorrencia.tel
    _ocorrencia.agente_id = ocorrencia.agente_id
    _ocorrencia.alerta_id = ocorrencia.alerta_id
    _ocorrencia.instituicao_id = ocorrencia.instituicao_id
    _ocorrencia.long = ocorrencia.long
    _ocorrencia.lati = ocorrencia.lati
    _ocorrencia.usuario_id = ocorrencia.usuario_id
    session.add(_ocorrencia)
    await session.commit()
    await session.refresh(_ocorrencia)
    return _ocorrencia

@router.delete("/{ocorrencia_id}", tags=["Ocorrências"], summary=["Deleta ocorrência"])
async def delete(ocorrencia_id: int,user: Usuario=Depends(obter_usuario_logado), session: AsyncSession = Depends(get_session) ) -> Response:
    _query = select(Ocorrencia).filter_by(id=ocorrencia_id)
    _result = await session.execute(_query)
    _ocorrencia: Optional[Ocorrencia] = _result.scalar_one_or_none()
    if not _ocorrencia:
        raise HTTPException(status_code=404, detail="Usuario not found")

    await session.delete(_ocorrencia)
    await session.commit()
    return JSONResponse({"deleted": f"{ocorrencia_id}"})
