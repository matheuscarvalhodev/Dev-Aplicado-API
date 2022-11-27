import uuid as uuid_pkg
from datetime import date, datetime
from typing import Optional

from pydantic import condecimal
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.sql import func
from sqlmodel import Column, DateTime, Field, SQLModel, String


class Ocorrencia(SQLModel, table=True):
    """
    id: int [PK]
    address: str [NN]
    name: str [OP]
    tel: str [OP]
    uuid_ocorrencia: uuid [OP]
    descricao: str [NN]
    long: str [OP]
    lati: str [OP]
    created_at: datetime [OP]
    agente_id: int [FK]
    alerta_id: int [FK] 
    instituicao_id: int [FK]
    usuario_id: int [FK]
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    address: str
    name: Optional[str] =  Field(default="anon")
    tel: Optional[str]
    uuid_ocorrencia: Optional[uuid_pkg.UUID] = Field(
        default_factory=uuid_pkg.uuid4,
        index=True,
    )
    descricao: Optional[str] = Field(sa_column=Column('descricao', TEXT), default=None)
    long: Optional[str]
    lati: Optional[str]
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    agente_id: Optional[int] = Field(default=None, foreign_key="usuario.id")
    alerta_id: Optional[int] = Field(default=None, foreign_key="notificacaoresposta.id")
    instituicao_id: int = Field(default=None, foreign_key="instituicaocompetente.id")
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")


class NotificacaoResposta(SQLModel, table=True):
    """
    id: int [PK]
    status: int [NN]
    created_at: datetime
    updated_at: datetime
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    status: Optional[int] = Field(default=0)
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
    descricao: str = Field(sa_column=Column('descricao', TEXT))
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
    tipo_usuario: int [OP] = 0-cidadão || 1-agente de fiscalização || 2-gerenciador || 3-administrador
    nome: str [NN]
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, sa_column=Column("username", String, unique=True))
    password: str
    cpf: str = Field(sa_column=Column("cpf", String, unique=True), index=True)
    tipo_usuario: Optional[int] = Field(default=1)
    nome: str
class UsuarioSignin(SQLModel):
    username: str
    password: str
    cpf: str
    nome: str

class UsuarioListagem(SQLModel):
    id: int
    username: str
    tipo_usuario: int
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
    id [PK]
    data [NN]
    nivel_agua [NN]
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    data: date
    nivel_agua: condecimal(max_digits=5, decimal_places=1) = Field(default=0)

class Previsao(SQLModel, table=True):
    """
    id [PK]
    nivel_agua [NN]
    create_at [NN]
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nivel_agua: condecimal(max_digits=5, decimal_places=1) = Field(default=0)
    create_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

class Anexos(SQLModel, table=True):
    """
    id [PK]
    url [NN]
    name [NN]
    ocorrencia_id [NN]
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    name: str
    ocorrencia_id: int= Field(foreign_key="ocorrencia.id")
    usuario_id: int= Field(foreign_key="usuario.id")

class Newsletter(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    body:str
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), nullable=True, server_default=func.now(), onupdate=datetime.now)
    )
