from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from sqlalchemy.orm import Session
from app.models.db import Base, engine, SessionLocal
from app.models.agendamento import Agendamento
from pydantic import BaseModel
from typing import Optional

# ----------------------------
# Inicializa FastAPI
# ----------------------------
app = FastAPI()

# ----------------------------
# Caminho da pasta PUBLIC
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
public_path = os.path.join(BASE_DIR, "public")

if not os.path.exists(public_path):
    print("ERRO: pasta public NÃO encontrada:", public_path)

app.mount("/public", StaticFiles(directory=public_path), name="public")

# ----------------------------
# CORS
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Banco de dados
# ----------------------------
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------
# Schemas
# ----------------------------
class AgendamentoCreate(BaseModel):
    nome: str
    telefone: str
    servico: str
    data: str
    horario: str


class AgendamentoUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    servico: Optional[str] = None
    data: Optional[str] = None
    horario: Optional[str] = None


# ----------------------------
# Rotas CRUD
# ----------------------------

@app.get("/agendamentos")
def listar(db: Session = Depends(get_db)):
    return db.query(Agendamento).all()


@app.post("/agendamentos")
def criar(data: AgendamentoCreate, db: Session = Depends(get_db)):
    novo = Agendamento(**data.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return {"mensagem": "Agendamento cadastrado com sucesso!"}


@app.patch("/agendamentos/{id}")
def atualizar(id: int, data: AgendamentoUpdate, db: Session = Depends(get_db)):
    agendamento = db.query(Agendamento).filter(Agendamento.id == id).first()
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(agendamento, campo, valor)

    db.commit()
    return {"mensagem": "Agendamento atualizado com sucesso!"}


@app.delete("/agendamentos/{id}")
def deletar(id: int, db: Session = Depends(get_db)):
    agendamento = db.query(Agendamento).filter(Agendamento.id == id).first()
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    db.delete(agendamento)
    db.commit()
    return {"mensagem": "Agendamento deletado com sucesso!"}


# ----------------------------
# Rota raiz — retorna index.html
# ----------------------------
@app.get("/")
def serve_frontend():
    index_file = os.path.join(public_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"erro": "index.html não encontrado dentro de /public"}
