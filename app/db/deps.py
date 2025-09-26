"""
Database dependencies for FastAPI dependency injection.

This module provides database session dependencies and related utilities.
"""

from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Get database session dependency.
    
    This is the main database dependency used throughout the application.
    It automatically handles opening and closing database sessions.
    
    Yields:
        SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db_session() -> Session:
    """
    Get a database session directly (not as a dependency).
    
    Warning: You must manually close this session when done.
    Use get_db() dependency in FastAPI routes instead.
    
    Returns:
        SQLAlchemy database session
    """
    return SessionLocal()