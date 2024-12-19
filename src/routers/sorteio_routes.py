import random
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.schemas import MatchRequest, Sorteio as SorteioSchema
from infra.sqlalchemy.repositorios.sorteios import SorteioRepositorio
from infra.sqlalchemy.repositorios.grupos import GrupoRepositorio
from infra.sqlalchemy.models.models import Usuario, Participacao, Sorteio
from infra.sqlalchemy.config.database import get_db
from uuid import UUID

router = APIRouter()

@router.post("/gerar_match")
def gerar_match(request: MatchRequest, db: Session = Depends(get_db)):
    grupo_id = request.grupo_id
    grupo_existe = GrupoRepositorio(db).buscar_por_id(grupo_id)
    if not grupo_existe:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    participantes = db.query(Usuario).join(Participacao).filter(Participacao.grupo_id == grupo_id).all()
    if len(participantes) < 2:
        raise HTTPException(status_code=400, detail="O grupo precisa ter pelo menos 2 participantes")
    random.shuffle(participantes)
    sorteios = []
    for i in range(len(participantes)):
        participante = participantes[i]
        amigo = participantes[(i + 1) % len(participantes)]
        sorteio = SorteioSchema(grupo_id=grupo_id, usuario_id=participante.id, amigo_id=amigo.id)
        sorteios.append(f"{participante.nome} sorteou {amigo.nome}")
    return {"resultado": sorteios}

@router.get("/resultados/{grupo_id}")
def obter_resultados(grupo_id: UUID, db: Session = Depends(get_db)):
    sorteios = db.query(Sorteio).filter(Sorteio.grupo_id == grupo_id).all()
    if not sorteios:
        raise HTTPException(status_code=404, detail="Nenhum sorteio encontrado para este grupo")
    return sorteios
