from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import _TemplateResponse

from project.app.auth import hash_provider, token_provider
from project.app.db import get_session
from project.app.models import Usuario, loginData
from project.app.settings import settings

Response = _TemplateResponse | RedirectResponse

router = APIRouter(prefix="/usuarios")


@router.get("/", response_model=list[Usuario])
async def ger_all(request: Request, session: AsyncSession = Depends(get_session), offset: int = 0, limit: int = Query(default=100, lte=100)) -> Response:
    _query = select(Usuario).offset(offset).limit(limit)
    _result = await session.execute(_query)
    courses = _result.scalars().all()
    return courses

@router.get("/{usuario_id}", response_model=Usuario)
async def get_user(request: Request, usuario_id: int, session: AsyncSession = Depends(get_session)) -> Response:
    _query = select(Usuario).filter_by(id=usuario_id)
    _result = await session.execute(_query)
    usuario: Optional[Usuario] = _result.scalar_one_or_none()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return usuario

@router.post("/", response_model=Usuario)
async def post_user(*, session: AsyncSession = Depends(get_session), usuario: Usuario) -> Response:
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

@router.post("/{usuario_id}", response_model=Usuario)
async def alter_user(usuario_id: int,usuario: Usuario, session: AsyncSession = Depends(get_session) ) -> Response:
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

@router.delete("/{usuario_id}")
async def delete_user(usuario_id: int, session: AsyncSession = Depends(get_session) ) -> Response:
    _query = select(Usuario).filter_by(id=usuario_id)
    _result = await session.execute(_query)
    _usuario: Optional[Usuario] = _result.scalar_one_or_none()
    if not _usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")

    await session.delete(_usuario)
    await session.commit()
    return JSONResponse({"message": f"{usuario_id}"})

@router.post("/token")
async def login(login_data: loginData, session: AsyncSession = Depends(get_session())) -> Response:
    _login = login_data.login_user
    _senha = login_data.pwd_user

    _query = select(loginData).filter_by(login=_login)
    _result = await session.execute(_query)
    _login_data: Optional[loginData] = _result.scalar_one_or_none()

    if not _login_data:
        raise HTTPException(status_code=404, detail="Usuario not found")
    
    _senha_valida = hash_provider.verificar_hash(_senha, _login_data.pwd_user)

    if not _senha_valida:
        raise HTTPException(status_code=404, detail="Login ou Senha incorretos")
    
    return _login_data

