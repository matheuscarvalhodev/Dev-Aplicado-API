from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

import uuid
class User(SQLModel, table=True):
    """
        TiposDeUsuarios:
        id
        login
        senha
        cpf
        tipos_de_usuarios
        nome
    """
    id: int = Field(default=None, primary_key=True)
    username: str 
    password: str
    cpf: int
    perms: int
    name: str

class Ocorrencia(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    address: str
    telefone: Optional[str]
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    cidadao_id: int
    agente_id: int
    uuid_ocorrencia = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alerta_id: int
    instituicao_id: int
    long: Optional[str]
    lati: Optional[str]


class tipoOcorrenciaAutuacao(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    prioridade: int
    tipo: str
    instituicao_id: int


class instituicaoCompetente(SQLModel, table=True):
    id: Field(default=None, primary_key=True)
    nome: str
    endereco: str
    telefone: int
    email: str