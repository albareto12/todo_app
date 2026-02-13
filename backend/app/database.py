"""
Configuración de la base de datos con SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# URL de conexión a la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://todouser:todopass@localhost:5432/tododb")

# Crear el engine de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crear SessionLocal para manejar sesiones de BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


# Dependencia para obtener la sesión de BD en los endpoints
def get_db():
    """
    Generador que proporciona una sesión de base de datos
    y asegura que se cierre después de usarla
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()