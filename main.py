from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
# Habilita CORS (igual ao cors() do Node)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Criar tabelas (equivalente ao Agendamento.sync())
# ----------------------------
Base.metadata.create_all(bind=engine)

# ----------------------------
# Dependência para criar sessão de banco (igual ao req.db do Node)
# ----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------------------
# Schemas Pydantic (para entrada/saída)
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
# ROTAS — CRUD COMPLETO (igual ao seu Express)
# ----------------------------

# GET /agendamentos — lista todos
@app.get("/agendamentos")
def listar_agendamentos(db: Session = Depends(get_db)):
    return db.query(Agendamento).all()


# POST /agendamentos — cria novo
@app.post("/agendamentos")
def criar_agendamento(data: AgendamentoCreate, db: Session = Depends(get_db)):
    novo = Agendamento(
        nome=data.nome,
        telefone=data.telefone,
        servico=data.servico,
        data=data.data,
        horario=data.horario
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return {"mensagem": "Agendamento cadastrado com sucesso!"}


# PATCH /agendamentos/:id — atualiza parcial
@app.patch("/agendamentos/{id}")
def atualizar_agendamento(id: int, data: AgendamentoUpdate, db: Session = Depends(get_db)):
    agendamento = db.query(Agendamento).filter(Agendamento.id == id).first()

    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    for campo, valor in data.dict(exclude_unset=True).items():
        setattr(agendamento, campo, valor)

    db.commit()
    return {"mensagem": "Agendamento atualizado com sucesso!"}


# DELETE /agendamentos/:id — deleta
@app.delete("/agendamentos/{id}")
def deletar_agendamento(id: int, db: Session = Depends(get_db)):
    agendamento = db.query(Agendamento).filter(Agendamento.id == id).first()

    if not agendamento:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")

    db.delete(agendamento)
    db.commit()
    return {"mensagem": "Agendamento deletado com sucesso!"}


# ----------------------------
# Rota raiz
# ----------------------------
@app.get("/")
def home():
    return {"status": "Servidor FastAPI funcionando!"}


