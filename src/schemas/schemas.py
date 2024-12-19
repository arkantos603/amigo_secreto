from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class Grupo(BaseModel):
    id: Optional[UUID] = None
    nome: str
    descricao: str
    data_sorteio: Optional[str] = None

class Usuario(BaseModel):
    id: Optional[UUID] = None
    nome: str
    email: str
    presente_fav: str

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    presente_fav: str

class Participacao(BaseModel):
    id: Optional[UUID] = None
    grupo_id: UUID
    usuario_id: UUID

class Sorteio(BaseModel):
    id: Optional[UUID] = None
    grupo_id: UUID
    usuario_id: UUID
    amigo_id: UUID

class MatchRequest(BaseModel):
    grupo_id: UUID

