from typing import List, Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import _TemplateResponse

from project.app.auth.utils import obter_usuario_logado
from project.app.db import get_session
from project.app.models import Previsao, Usuario, UsuarioListagem
from project.app.settings import settings

Response = _TemplateResponse | RedirectResponse

router = APIRouter(prefix="/usuarios")


@router.get("/", response_model=List[UsuarioListagem], tags=["Usuários"], summary=["Lista todos os usuários"])
async def list(request: Request, user: Usuario=Depends(obter_usuario_logado), session: AsyncSession = Depends(get_session), offset: int = 0, limit: int = Query(default=100, lte=100)) -> Response:
    _query = select(Usuario).offset(offset).limit(limit)
    _result = await session.execute(_query)
    _usuario = _result.scalars().all()
    return _usuario

@router.get("/{usuario_id}", response_model=UsuarioListagem, tags=["Usuários"], summary=["Lista o usuáro a partir do id"])
async def by_id(request: Request, usuario_id: int, session: AsyncSession = Depends(get_session)) -> Response:
    _query = select(Usuario).filter_by(id=usuario_id)
    _result = await session.execute(_query)
    usuario: Optional[Usuario] = _result.scalar_one_or_none()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return usuario

@router.post("/", response_model=UsuarioListagem, tags=["Usuários"], summary=["Cria um novo usuário"])
async def create(*, session: AsyncSession = Depends(get_session), usuario: Usuario) -> Response:
    usuario = Usuario(
        login= usuario.login, 
        senha= usuario.senha, 
        cpf= usuario.cpf, 
        tipo_usuario= usuario.tipo_usuario, 
        nome= usuario.nome
        )
    session.add(usuario)
    await session.commit()
    await session.refresh(usuario)
    return usuario

@router.post("/{usuario_id}", response_model=UsuarioListagem, tags=["Usuários"], summary=["Atualiza as informações do usuário"])
async def update(usuario_id: int,usuario: Usuario, session: AsyncSession = Depends(get_session) ) -> Response:
    _query = select(Usuario).filter_by(id=usuario_id)
    _result = await session.execute(_query)
    _usuario: Optional[Usuario] = _result.scalar_one_or_none()
    if not _usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")
    _usuario.login =usuario.login 
    _usuario.senha =usuario.senha 
    _usuario.cpf =usuario.cpf 
    _usuario.tipo_usuario =usuario.tipo_usuario
    _usuario.nome =usuario.nome
    session.add(_usuario)
    await session.commit()
    await session.refresh(_usuario)
    return _usuario

@router.delete("/{usuario_id}", tags=["Usuários"], summary=["Deleta o usuário"])
async def delete(usuario_id: int, session: AsyncSession = Depends(get_session) ) -> Response:
    _query = select(Usuario).filter_by(id=usuario_id)
    _result = await session.execute(_query)
    _usuario: Optional[Usuario] = _result.scalar_one_or_none()
    if not _usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")

    await session.delete(_usuario)
    await session.commit()
    return JSONResponse({"message": f"{usuario_id}"})

