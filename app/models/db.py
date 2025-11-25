import os
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")


DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}  # OBRIGATÓRIO NO RENDER
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
