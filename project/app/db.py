from datetime import date
from random import choice, randint, uniform
from typing import AsyncGenerator, Optional

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from project.app.auth import hash_provider
from project.app.models import (DadosHistoricos, InstituicaoCompetente,
                                NotificacaoResposta, Ocorrencia, Previsao,
                                TipoOcorrenciaAutuacao, Usuario)
from project.app.settings import settings

global engine  # pylint: disable=global-at-module-level
engine: Optional[AsyncEngine] = None

def get_engine() -> AsyncEngine:
    global engine  # pylint: disable=global-statement
    if engine is None:

        engine = create_async_engine(
            settings.SQLALCHEMY_DATABASE_URI, echo=settings.SQLALCHEMY_ECHO, future=True
        )
    return engine


async def init_db() -> None:
    async with get_engine().begin() as conn:
        # uncomment line below if you want the database to be flushed
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
    async_session = sessionmaker(
        get_engine(), class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        await create_data(session)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        get_engine(), class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


async def create_data(session: AsyncSession) -> None:
    """
    Generate random data for tests.
    """
    # for i in range(10):
        # u = Usuario(login=f"login{i+1}", senha=f"senha{i+1}", cpf=f"{99999999990+i}", tipo_usuario=choice(["cidadao", "funcionario", "administrador"]), nome=f"Nome {i+1}")
        # session.add(u)

    for i in range(5):
        passh = hash_provider.gerar_hash(f"senha{i+1}")
        ld = Usuario(
            username=f"username{i+1}",
            password=passh,
            cpf=f"1231231231{i+1}",
            tipo_usuario=choice([0,1,2,3,4]),
            nome=f"Usuário {i+1}",
            )
        session.add(ld)
        ic = InstituicaoCompetente(
            name=f"Instituto {i+1}",
            address=f"Rua {i+1}, Nº 123",
            tel="(93) 112312312",
            email=f"instituto{i+1}@email.com"
            )
        session.add(ic)
        n_agua = round(uniform(33.3, 66.6), 1)
        data_random = date(2018, 6, i+1)
        dh = DadosHistoricos(
                data=data_random, 
                nivel_agua=n_agua
                )
        session.add(dh)
        p = Previsao(
                nivel_agua=n_agua
                )
        session.add(p)
        no = NotificacaoResposta(
                status=choice([0,1,2,3,4])
                )
        session.add(no)
        oc = Ocorrencia(
            address=f"Rua {i+1}, N°: 1231"
        )
        session.add(oc)
        to = TipoOcorrenciaAutuacao(
            nome=f"Nome {i+1}",
            descricao=f"descricao {i+1}",
            prioridade=choice([0,1,2,3,4]),
            tipo=f"Tipo {i+1}"
        )
        session.add(to)
    
    await session.commit()