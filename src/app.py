from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import usuarios_routes, grupos_routes, participante_routes, sorteio_routes
from infra.sqlalchemy.config.database import criar_bd

app = FastAPI()

criar_bd()

origins = ['http://localhost:5500', 'http://127.0.0.1:5500']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios_routes.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(grupos_routes.router, prefix="/grupos", tags=["Grupos"])
app.include_router(participante_routes.router, prefix="/participacoes", tags=["Participacoes"])
app.include_router(sorteio_routes.router, prefix="/sorteios", tags=["Sorteios"])

@app.get("/")
def home():
    return {"message": "Bem-vindo à API de Amigo Oculto!"}
