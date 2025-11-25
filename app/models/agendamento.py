from sqlalchemy import Column, Integer, String
from app.models.db import Base

class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    servico = Column(String, nullable=False)
    data = Column(String, nullable=False)      # <-- string
    horario = Column(String, nullable=False)   # <-- string
