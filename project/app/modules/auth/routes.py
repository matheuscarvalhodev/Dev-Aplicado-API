from typing import List, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import _TemplateResponse

from project.app.auth import hash_provider, token_provider
from project.app.auth.utils import obter_usuario_logado
from project.app.db import get_session
from project.app.models import (LoginData, LoginSucesso, Usuario,
                                UsuarioSignin, UsuarioSimples)

Response = _TemplateResponse | RedirectResponse

router = APIRouter(prefix="/auth")

print("aaaa")

@router.post('/signup',
             status_code=status.HTTP_201_CREATED,
             response_model=UsuarioSimples, tags=["Autorização"], summary=["Registro de usuário"])
async def signup(usuario: UsuarioSignin, session: AsyncSession = Depends(get_session)):
    _username = usuario.username
    _password = hash_provider.gerar_hash(usuario.password)
    _cpf = usuario.cpf
    _nome = usuario.nome

    _query = select(Usuario).filter_by(username=_username)
    _result = await session.execute(_query)
    is_username: Optional[Usuario] = _result.scalar_one_or_none()
    if is_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Já existe um usuário para este nome de usuário')

    _query = select(Usuario).filter_by(cpf=_cpf)
    _result = await session.execute(_query)
    is_cpf: Optional[Usuario] = _result.scalar_one_or_none()
    if is_cpf:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Já existe um usuário para este CPF')

    u = Usuario(username=_username, password=_password, cpf=_cpf, nome=_nome)
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return u


@router.post("/token",response_model=LoginSucesso, tags=["Autorização"], summary=["Login de usuário"])
async def login(req: Request, session: AsyncSession = Depends(get_session)) -> Response:
    if req.headers['Content-Type'] not in ['application/json', 'application/x-www-form-urlencoded']:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Tipo de conteúdo não suportado')
    elif req.headers['Content-Type']  == 'application/json': 
        body = await req.json()
    elif req.headers['Content-Type']  == 'application/x-www-form-urlencoded': 
        body = await req.form()
    [_username,_password] = [body["username"], body["password"]]
    _query = select(Usuario).filter_by(username=_username)
    _result = await session.execute(_query)
    is_username: Optional[Usuario] = _result.scalar_one_or_none()
    if not is_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Usuário ou senha estão incorretos')
    valid_password = hash_provider.verificar_hash(_password,is_username.password)
    if not valid_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Usuário ou senha estão incorretos')
    token = token_provider.criar_access_token({'sub': _username})
    return LoginSucesso(usuario=is_username, access_token=token)


"""
    Para incluir autenticação na rota, deve ser incluído a dependência do modelo no fator de login
"""
@router.get("/me", response_model=UsuarioSimples, tags=["Autenticação"], summary=["Verifica se o token do usuário é válido"])
def me(usuario: Usuario=Depends(obter_usuario_logado)):
    return usuario