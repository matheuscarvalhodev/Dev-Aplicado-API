import uuid as uuid_pkg
from datetime import date, datetime
from typing import Optional

from pydantic import condecimal
from sqlalchemy.sql import func
from sqlmodel import Column, DateTime, Field, SQLModel, String


class Ocorrencia(SQLModel, table=True):
    """
    id: int [PK]
    address: str [NN]
    name: str [OP]
    tel: str [OP]
    uuid_ocorrencia: uuid 
    long: str [OP]
    lati: str [OP]
    created_at: datetime 
    agente_id: int [FK]
    alerta_id: int [FK] 
    instituicao_id: int [FK]
    usuario_id: int [FK]
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    address: str
    name: Optional[str] =  Field(default="anon")
    tel: Optional[str]
    uuid_ocorrencia: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    long: Optional[str]
    lati: Optional[str]
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    agente_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    alerta_id: Optional[int] = Field(default=None, foreign_key="notificacaoresposta.id")
    instituicao_id: Optional[int] = Field(default=None, foreign_key="instituicaocompetente.id")
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")


class NotificacaoResposta(SQLModel, table=True):
    """
    id: int [PK]
    status: str [NN]
    created_at: datetime
    updated_at: datetime
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    status: Optional[int] =  Field(default=0)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True, server_default=func.now(), onupdate=datetime.now)
    )


class TipoOcorrenciaAutuacao(SQLModel, table=True):
    """
    id: int [PK]
    nome: str [NN]
    descricao: str [NN]
    prioridade: int [NN] = 1-5
    tipo: str [NN]
    instituicao_id: int [FK]
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    prioridade: int
    tipo: str
    instituicao_id: Optional[int] = Field(default=None, foreign_key="instituicaocompetente.id")

class InstituicaoCompetente(SQLModel, table=True):
    """
    id: int [PK]
    name: str [NN]
    address: str [NN]
    tel: str [OP]
    email: str [OP]
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: str
    tel: Optional[str]
    email: Optional[str]

class Usuario(SQLModel, table=True):
    """
    id: int [PK]
    username: str [NN]
    password: str [NN]
    cpf: str [NN]
    tipo_usuario: int [OP] = 0-convidado || 1-cidadão || 2-agente de fiscalização || 3-gerenciador || 4-administrador
    nome: str [NN]
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, sa_column=Column("username", String, unique=True))
    password: str
    cpf: str = Field(sa_column=Column("cpf", String, unique=True), index=True)
    tipo_usuario: Optional[int] = Field(default=0)
    nome: str


class UsuarioSimples(SQLModel):
    username: str
    nome: str


class LoginData(SQLModel):
    username: str
    password: str

class LoginSucesso(SQLModel):
    usuario: UsuarioSimples
    access_token: str

class DadosHistoricos(SQLModel, table=True):
    """
    id
    data
    nivel_agua
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    data: date
    nivel_agua: condecimal(max_digits=5, decimal_places=1) = Field(default=0)

class Previsao(SQLModel, table=True):
    """
    id
    nivel_agua
    create_at
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nivel_agua: condecimal(max_digits=5, decimal_places=1) = Field(default=0)
    create_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )