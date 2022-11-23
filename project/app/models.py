import uuid as uuid_pkg
from datetime import datetime
from typing import Optional

from sqlalchemy.sql import func
from sqlmodel import Column, DateTime, Field, SQLModel


class Usuario(SQLModel, table=True):
    """
        args:
        login,
        senha,
        cpf,
        tipo_usuario,
        nome
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    login: str 
    senha: str
    cpf: str
    tipo_usuario: str
    nome: str

class Ocorrencia(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    address: str
    telefone: Optional[str]
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    uuid_ocorrencia: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    cidadao_id: int
    agente_id: int
    alerta_id: int
    instituicao_id: int
    long: Optional[str]
    lati: Optional[str]
    user_id: Optional[int] = Field(default=None, foreign_key="usuario.id")


class tipoOcorrenciaAutuacao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    prioridade: int
    tipo: str
    instituicao_id: int


class instituicaoCompetente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    endereco: str
    telefone: int
    email: str