from sqlalchemy.orm import Session
from schemas import schemas
from infra.sqlalchemy.models import models
from uuid import UUID

class ParticipacaoRepositorio:
    def __init__(self, db: Session):
        self.db = db

    def listar_por_grupo(self, grupo_id: UUID):
        return self.db.query(models.Participacao).filter(models.Participacao.grupo_id == grupo_id).all()

    def salvar(self, participacao: schemas.Participacao):
        participacao_bd = models.Participacao(
            grupo_id=participacao.grupo_id,
            usuario_id=participacao.usuario_id
        )
        self.db.add(participacao_bd)
        self.db.commit()
        self.db.refresh(participacao_bd)
        return participacao_bd