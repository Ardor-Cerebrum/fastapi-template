"""
Database connection and session management.

This module sets up SQLAlchemy engine, session factory, and base model class.
"""

import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings

logger = logging.getLogger(__name__)

NO_DB_SET_ERROR = "DATABASE_URL is not set"

# Create SQLAlchemy engine
engine = None
if not settings.DATABASE_URL:
    logger.warning(NO_DB_SET_ERROR)
elif settings.DATABASE_URL.startswith("sqlite"):
    # SQLite specific configuration
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DEBUG,
    )
else:
    # PostgreSQL, MySQL, etc.
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_size=20,
        max_overflow=0,
        pool_recycle=300,
        echo=settings.DEBUG,
    )

# Create SessionLocal class
SessionLocal = None
if engine:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

def get_db():
    """
    Database dependency for FastAPI.

    Yields:
        Database session
    """
    if not SessionLocal:
        logger.warning(f"Cannot get session {NO_DB_SET_ERROR}.")
        return

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all database tables."""
    if not engine:
        logger.warning(f"Cannot create database tables {NO_DB_SET_ERROR}.")
        return
    Base.metadata.create_all(bind=engine)
