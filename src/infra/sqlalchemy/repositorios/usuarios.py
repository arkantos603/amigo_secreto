# filepath: /home/joao/Documentos/python_codes/amigo_secreto/src/infra/sqlalchemy/repositorios/usuarios.py
from sqlalchemy.orm import Session
from schemas import schemas
from infra.sqlalchemy.models import models
from uuid import UUID

class UsuarioRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        return self.db.query(models.Usuario).all()

    def salvar(self, usuario: schemas.UsuarioCreate):
        usuario_bd = models.Usuario(
            nome=usuario.nome,
            email=usuario.email,
            presente_fav=usuario.presente_fav
        )
        self.db.add(usuario_bd)
        self.db.commit()
        self.db.refresh(usuario_bd)
        return usuario_bd

    def buscar_por_id(self, usuario_id: UUID):
        return self.db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

    def buscar_por_email(self, email: str):
        return self.db.query(models.Usuario).filter(models.Usuario.email == email).first()

    def remover(self, usuario_id: UUID):
        usuario_bd = self.db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
        if usuario_bd:
            self.db.delete(usuario_bd)
            self.db.commit()
            return usuario_bd
        return None