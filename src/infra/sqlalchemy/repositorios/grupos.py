from sqlalchemy.orm import Session
from schemas import schemas
from infra.sqlalchemy.models import models
from uuid import UUID

class GrupoRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        return self.db.query(models.Grupo).all()

    def listar_com_usuarios(self):
        grupos = self.db.query(models.Grupo).all()
        grupos_com_usuarios = []
        for grupo in grupos:
            usuarios = self.db.query(models.Usuario).join(models.Participacao).filter(models.Participacao.grupo_id == grupo.id).all()
            grupos_com_usuarios.append({
                "grupo": grupo,
                "usuarios": usuarios
            })
        return grupos_com_usuarios

    def salvar(self, grupo: schemas.Grupo):
        grupo_bd = models.Grupo(
            nome=grupo.nome,
            descricao=grupo.descricao,
            data_sorteio=grupo.data_sorteio
        )
        self.db.add(grupo_bd)
        self.db.commit()
        self.db.refresh(grupo_bd)
        return grupo_bd

    def buscar_por_id(self, grupo_id: UUID):
        return self.db.query(models.Grupo).filter(models.Grupo.id == grupo_id).first()

    def remover(self, grupo_id: UUID):
        grupo_bd = self.db.query(models.Grupo).filter(models.Grupo.id == grupo_id).first()
        if grupo_bd:
            self.db.delete(grupo_bd)
            self.db.commit()
            return grupo_bd
        return None