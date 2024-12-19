from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from infra.sqlalchemy.config.database import get_db
from schemas.schemas import Participacao as ParticipacaoSchema
from infra.sqlalchemy.repositorios.participacoes import ParticipacaoRepositorio
from infra.sqlalchemy.repositorios.usuarios import UsuarioRepositorio
from infra.sqlalchemy.repositorios.grupos import GrupoRepositorio
from infra.sqlalchemy.models.models import Participacao

router = APIRouter()

@router.post("/add_amigo")
def add_amigo(participacao: ParticipacaoSchema, db: Session = Depends(get_db)):
    usuario_existe = UsuarioRepositorio(db).buscar_por_id(participacao.usuario_id)
    if not usuario_existe:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    grupo_existe = GrupoRepositorio(db).buscar_por_id(participacao.grupo_id)
    if not grupo_existe:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    
    participacao_existe = db.query(Participacao).filter(
        Participacao.usuario_id == participacao.usuario_id,
        Participacao.grupo_id == participacao.grupo_id
    ).first()
    if participacao_existe:
        raise HTTPException(status_code=400, detail="Usuário já está no grupo")

    return ParticipacaoRepositorio(db).salvar(participacao)
