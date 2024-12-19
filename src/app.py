import random
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from infra.sqlalchemy.config.database import get_db, criar_bd
from schemas.schemas import Grupo as GrupoSchema, UsuarioCreate as UsuarioSchema, Participacao as ParticipacaoSchema, Sorteio as SorteioSchema, MatchRequest
from infra.sqlalchemy.repositorios.grupos import GrupoRepositorio
from infra.sqlalchemy.repositorios.usuarios import UsuarioRepositorio
from infra.sqlalchemy.repositorios.participacoes import ParticipacaoRepositorio
from infra.sqlalchemy.repositorios.sorteios import SorteioRepositorio
from infra.sqlalchemy.models.models import Usuario, Participacao, Sorteio
from uuid import UUID

app = FastAPI()

criar_bd()

origins = ['http://localhost:5500', 'http://127.0.0.1:5500']

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Bem-vindo à API de Amigo Oculto!"}

# Rota para cadastrar usuários (amigos)
@app.post("/cadastrar_amigo")
def cadastrar_amigo(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    usuario_existente = UsuarioRepositorio(db).buscar_por_email(usuario.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    usuario_criado = UsuarioRepositorio(db).salvar(usuario)
    return usuario_criado

# Rota para listar perfis de usuários
@app.get("/perfis")
def listar_perfis(db: Session = Depends(get_db)):
    perfis = UsuarioRepositorio(db).listar()
    return perfis

# Rota para criar grupos
@app.post("/criar_grupo")
def criar_grupo(grupo: GrupoSchema, db: Session = Depends(get_db)):
    grupo_criado = GrupoRepositorio(db).salvar(grupo)
    return grupo_criado

# Rota para adicionar amigos a um grupo
@app.post("/add_amigo")
def add_amigo(participacao: ParticipacaoSchema, db: Session = Depends(get_db)):
    usuario_existe = UsuarioRepositorio(db).buscar_por_id(participacao.usuario_id)
    if not usuario_existe:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    grupo_existe = GrupoRepositorio(db).buscar_por_id(participacao.grupo_id)
    if not grupo_existe:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")
    
    # Verificar se o usuário já está no grupo
    participacao_existe = db.query(Participacao).filter(
        Participacao.usuario_id == participacao.usuario_id,
        Participacao.grupo_id == participacao.grupo_id
    ).first()
    if participacao_existe:
        raise HTTPException(status_code=400, detail="Usuário já está no grupo")

    participacao_criada = ParticipacaoRepositorio(db).salvar(participacao)
    return {
        "message": f"Usuário {usuario_existe.nome} cadastrado com sucesso em {grupo_existe.nome}",
        "participacao": {
            "id": participacao_criada.id,
            "grupo_id": participacao_criada.grupo_id,
            "usuario_id": participacao_criada.usuario_id
        }
    }

# Rota para obter grupos com usuários
@app.get("/grupos")
def obter_grupos(db: Session = Depends(get_db)):
    grupos_com_usuarios = GrupoRepositorio(db).listar_com_usuarios()
    return grupos_com_usuarios

# Rota para gerar o match (sorteio)
@app.post("/gerar_match")
def gerar_match(request: MatchRequest, db: Session = Depends(get_db)):
    grupo_id = request.grupo_id

    grupo_existe = GrupoRepositorio(db).buscar_por_id(grupo_id)
    if not grupo_existe:
        raise HTTPException(status_code=404, detail="Grupo não encontrado")

    participantes = db.query(Usuario).join(Participacao).filter(Participacao.grupo_id == grupo_id).all()
    total_participantes = len(participantes)

    if total_participantes < 2:
        raise HTTPException(status_code=400, detail="O grupo precisa ter pelo menos 2 participantes para realizar o sorteio")

    if total_participantes % 2 != 0:
        raise HTTPException(status_code=400, detail="O grupo precisa ter uma quantidade par de membros para realizar o sorteio")

    sorteios_existentes = SorteioRepositorio(db).listar_por_grupo(grupo_id)
    if sorteios_existentes:
        raise HTTPException(status_code=400, detail="O sorteio já foi realizado para este grupo")
    
    random.shuffle(participantes)
    sorteios = []

    for i in range(total_participantes):
        participante = participantes[i]
        amigo = participantes[(i + 1) % total_participantes]
        sorteio = SorteioSchema(grupo_id=grupo_id, usuario_id=participante.id, amigo_id=amigo.id)
        sorteios.append(f"{participante.nome} sorteou {amigo.nome}")

    return {"resultado": sorteios}


@app.get("/resultados/{grupo_id}")
def obter_resultados(grupo_id: UUID, db: Session = Depends(get_db)):
    sorteios = db.query(Sorteio).filter(Sorteio.grupo_id == grupo_id).all()
    if not sorteios:
        raise HTTPException(status_code=404, detail="Nenhum sorteio encontrado para este grupo")

    resultados = []
    for sorteio in sorteios:
        usuario = db.query(Usuario).filter(Usuario.id == sorteio.usuario_id).first()
        amigo = db.query(Usuario).filter(Usuario.id == sorteio.amigo_id).first()
        resultados.append(f"{usuario.nome} sorteou {amigo.nome} (Presente favorito: {amigo.presente_fav})")
    return resultados