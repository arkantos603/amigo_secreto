from sqlalchemy.orm import Session
from schemas import schemas
from infra.sqlalchemy.models import models
from uuid import UUID

class SorteioRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, sorteio: schemas.Sorteio):
        sorteio_bd = models.Sorteio(
            grupo_id=sorteio.grupo_id,
            usuario_id=sorteio.usuario_id,
            amigo_id=sorteio.amigo_id
        )
        self.db.add(sorteio_bd)
        self.db.commit()
        self.db.refresh(sorteio_bd)
        return sorteio_bd

    def listar_por_grupo(self, grupo_id: UUID):
        return self.db.query(models.Sorteio).filter(models.Sorteio.grupo_id == grupo_id).all()