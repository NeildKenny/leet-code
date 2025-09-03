"""Database utilities for the DnD Notebook backend."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Using a local SQLite database for simplicity
DATABASE_URL = "sqlite:///backend.db"

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)

Base = declarative_base()


def create_tables() -> None:
    """Create database tables based on defined models."""
    Base.metadata.create_all(bind=engine)
