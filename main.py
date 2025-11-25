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

app = FastAPI()

# ---------------------------------------------------------
# Caminho correto da pasta public dentro de /app/public
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # /opt/render/project/src/app
public_path = os.path.join(BASE_DIR, "public")          # /opt/render/project/src/app/public

print("PUBLIC PATH:", public_path)
print("EXISTS:", os.path.exists(public_path))

# Só monta se existir
if os.path.exists(public_path):
    app.mount("/public", StaticFiles(directory=public_path), name="public")
else:
    print(f"⚠️ Aviso: pasta public NÃO encontrada em {public_path}")

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Banco
# ---------------------------------------------------------
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------------------------------------
# Schemas
# ---------------------------------------------------------
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

# ---------------------------------------------------------
# CRUD
# ---------------------------------------------------------

@app.get("/agendamentos")
def listar_agendamentos(db: Session = Depends(get_db)):
    return db.query(Agendamento).all()

@app.post("/agendamentos")
def criar_agendamento(data: AgendamentoCreate, db: Session = Depends(get_db)):
    novo = Agendamento(**data.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return {"mensagem": "Agendamento cadastrado com sucesso!"}

@app.patch("/agendamentos/{id}")
def atualizar_agendamento(id: int, data: AgendamentoUpdate, db: Session = Depends(get_db)):
    agendamento = db.query(Agendamento).filter(Agendamento.id == id).first()
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(agendamento, campo, valor)

    db.commit()
    return {"mensagem": "Agendamento atualizado com sucesso!"}

@app.delete("/agendamentos/{id}")
def deletar_agendamento(id: int, db: Session = Depends(get_db)):
    agendamento = db.query(Agendamento).filter(Agendamento.id == id).first()
    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    db.delete(agendamento)
    db.commit()
    return {"mensagem": "Agendamento deletado com sucesso!"}

# ---------------------------------------------------------
# Rota raiz → devolve index.html
# ---------------------------------------------------------

@app.get("/")
def root():
    index_path = os.path.join(public_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "Servidor FastAPI funcionando, mas index.html não encontrado."}
