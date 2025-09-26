"""
API dependencies for FastAPI routes.

This module provides basic dependencies used across API routes.
"""

from fastapi import Query
from sqlalchemy.orm import Session

from app.db.deps import get_db


# Basic pagination dependency
def get_pagination_params(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records to return")
) -> dict:
    """
    Get pagination parameters from query parameters.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        Dictionary with pagination parameters
    """
    return {"skip": skip, "limit": limit}
