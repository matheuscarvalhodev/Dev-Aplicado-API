from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import _TemplateResponse

from project.app.auth.utils import obter_usuario_logado
from project.app.db import get_session
from project.app.models import InstituicaoCompetente, Previsao, Usuario
from project.app.settings import settings

Response = _TemplateResponse | RedirectResponse

router = APIRouter(prefix="/instituicoes")


@router.get("", response_model=List[InstituicaoCompetente])
async def list(request: Request, user: Usuario=Depends(obter_usuario_logado), session: AsyncSession = Depends(get_session), offset: int = 0, limit: int = Query(default=100, lte=100)) -> Response:
    print(user)
    _query = select(InstituicaoCompetente).offset(offset).limit(limit)
    _result = await session.execute(_query)
    _instituicao = _result.scalars().all()
    return _instituicao

@router.get("/{instituicao_id}", response_model=InstituicaoCompetente)
async def by_id(request: Request, instituicao_id: int, session: AsyncSession = Depends(get_session)) -> Response:
    _query = select(InstituicaoCompetente).filter_by(id=instituicao_id)
    _result = await session.execute(_query)
    _instituicao: Optional[InstituicaoCompetente] = _result.scalar_one_or_none()
    if not _instituicao:
        raise HTTPException(status_code=404, detail="Instituicao not found")
    return _instituicao

@router.post("/", response_model=InstituicaoCompetente)
async def create(*, session: AsyncSession = Depends(get_session), instituicao: InstituicaoCompetente) -> Response:
    _instituicao = InstituicaoCompetente(
        name=instituicao.name,
        address=instituicao.address,
        tel=instituicao.tel,
        email=instituicao.email
        )
    session.add(_instituicao)
    await session.commit()
    await session.refresh(_instituicao)
    return _instituicao

@router.post("/{instituicao_id}", response_model=InstituicaoCompetente)
async def update(instituicao_id: int,instituicao: InstituicaoCompetente, session: AsyncSession = Depends(get_session) ) -> Response:
    _query = select(InstituicaoCompetente).filter_by(id=instituicao_id)
    _result = await session.execute(_query)
    _instituicao: Optional[InstituicaoCompetente] = _result.scalar_one_or_none()
    if not _instituicao:
        raise HTTPException(status_code=404, detail="Instituicao not found")
    _instituicao.name = instituicao.name
    _instituicao.address = instituicao.address
    _instituicao.tel = instituicao.tel
    _instituicao.email = instituicao.email
    session.add(_instituicao)
    await session.commit()
    await session.refresh(_instituicao)
    return _instituicao

@router.delete("/{instituicao_id}")
async def delete(instituicao_id: int, session: AsyncSession = Depends(get_session) ) -> Response:
    _query = select(InstituicaoCompetente).filter_by(id=instituicao_id)
    _result = await session.execute(_query)
    _instituicao: Optional[InstituicaoCompetente] = _result.scalar_one_or_none()
    if not _instituicao:
        raise HTTPException(status_code=404, detail="Instituicao not found")

    await session.delete(_instituicao)
    await session.commit()
    return JSONResponse({"deleted": f"{instituicao_id}"})

