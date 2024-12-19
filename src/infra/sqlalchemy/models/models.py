from sqlalchemy import Column, String, ForeignKey, Table, MetaData
from sqlalchemy.dialects.postgresql import UUID
from infra.sqlalchemy.config.database import Base
import uuid

metadata = MetaData()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    presente_fav = Column(String)

class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)
    data_sorteio = Column(String)

class Participacao(Base):
    __tablename__ = "participacoes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    grupo_id = Column(UUID(as_uuid=True), ForeignKey("grupos.id"))
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))

class Sorteio(Base):
    __tablename__ = "sorteios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    grupo_id = Column(UUID(as_uuid=True), ForeignKey("grupos.id"))
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    amigo_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))