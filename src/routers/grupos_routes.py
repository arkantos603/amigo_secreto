from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from infra.sqlalchemy.config.database import get_db
from schemas.schemas import Grupo as GrupoSchema
from infra.sqlalchemy.repositorios.grupos import GrupoRepositorio

router = APIRouter()

@router.post("/criar_grupo")
def criar_grupo(grupo: GrupoSchema, db: Session = Depends(get_db)):
    return GrupoRepositorio(db).salvar(grupo)

@router.get("/grupos")
def obter_grupos(db: Session = Depends(get_db)):
    return GrupoRepositorio(db).listar_com_usuarios()
