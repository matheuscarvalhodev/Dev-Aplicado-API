import uuid as uuid_pkg
from datetime import date, datetime
from typing import Optional

from pydantic import condecimal
from sqlalchemy.sql import func
from sqlmodel import Column, DateTime, Field, SQLModel, String


class Ocorrencia(SQLModel, table=True):
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
    agente_id: int
    alerta_id: int
    instituicao_id: Optional[int] = Field(default=None, foreign_key="instituicaocompetente.id")
    long: Optional[str]
    lati: Optional[str]
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")



class TipoOcorrenciaAutuacao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    prioridade: int
    tipo: str
    instituicao_id: Optional[int] = Field(default=None, foreign_key="instituicaocompetente.id")

class InstituicaoCompetente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    address: str
    tel: int
    email: str

class Usuario(SQLModel, table=True):
    """
    args*:
    username
    password
    cpf
    tipo_usuario: 0 = convidado || 1 = cidadão || 2 = agente de fiscalização || 3 = gerenciador || 4 = administrador
    nome
    ('nattan', '12312312312', '$2b$12$izCZTtzftVB/k1GU1UX9muQlpx4oia102AuGSf6cf0vJNNlrJ4UcO', 0, 'Nattan Lobato')
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
    id: Optional[int] = Field(default=None, primary_key=True)
    data: date
    nivel_agua: condecimal(max_digits=5, decimal_places=1) = Field(default=0)

class Previsao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nivel_agua: condecimal(max_digits=5, decimal_places=1) = Field(default=0)
    create_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )