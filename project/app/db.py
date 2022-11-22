from datetime import date
from random import choice, randint
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from project.app.models import Usuario 

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
    #     u = Usuario(
    #     login=f"login{i}",
    #     senha=f"senha{i}",      
    #     cpf=9999999999+(i+1),
    #     tipos_de_usuarios=choice(["cidadao", "funcionario", "agente"]),
    #     nome=f"Nome {i+1}",
    #     )
       
    #     session.add(u)

    await session.commit()
