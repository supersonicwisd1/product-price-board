# app/db/base.py
from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
import importlib



# Engine setup
# engine = create_engine(
#     settings.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
# )
# Use PostgreSQL for development
# engine = create_engine(settings.DATABASE_URL)

# Session maker
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def load_models():
    # Ensure all models in app.models/__init__.py are loaded
    importlib.import_module("app.models")