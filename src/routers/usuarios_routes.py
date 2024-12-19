from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from infra.sqlalchemy.config.database import get_db
from schemas.schemas import UsuarioCreate as UsuarioSchema
from infra.sqlalchemy.repositorios.usuarios import UsuarioRepositorio

router = APIRouter()

@router.post("/cadastrar_amigo")
def cadastrar_amigo(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    usuario_existente = UsuarioRepositorio(db).buscar_por_email(usuario.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    return UsuarioRepositorio(db).salvar(usuario)

@router.get("/perfis")
def listar_perfis(db: Session = Depends(get_db)):
    return UsuarioRepositorio(db).listar()
