from sqlalchemy import create_engine
import os
from dotenv import load_dotenv   # ← IMPORTANTE

# Carrega as variáveis do arquivo .env
load_dotenv()      # ← SEM ISSO o Python não lê o .env

# Apenas para debug
print("DB_USER =", os.getenv("DB_USER"))
print("DB_PASS =", os.getenv("DB_PASS"))
print("DB_HOST =", os.getenv("DB_HOST"))
print("DB_NAME =", os.getenv("DB_NAME"))

DATABASE_URL = (
    f"postgresql+psycopg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}?sslmode=require"
)

print("URL gerada:", DATABASE_URL)

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("Conectado com sucesso!")
except Exception as erro:
    print("Erro ao conectar:", erro)
