from typing import Optional

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from project.app.auth import token_provider
from project.app.db import get_session
from project.app.models import Usuario

oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/token')


async def obter_usuario_logado(token: str = Depends(oauth2_schema),
                         session: AsyncSession = Depends(get_session)):
    # decodificar o token, pegar o telefone, buscar usuario no bd e retornar
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')

    try:
        _username = token_provider.verificar_access_token(token)
    except JWTError:
        raise exception
    if not _username:
        raise exception

    _query = select(Usuario).filter_by(username=_username)
    _result = await session.execute(_query)
    is_usuario: Optional[Usuario] = _result.scalar_one_or_none()
    if not is_usuario:
        raise exception

    return is_usuario