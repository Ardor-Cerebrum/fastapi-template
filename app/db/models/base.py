"""
Base model class with common fields and utilities.

This module provides a base model class that includes common fields
like id, created_at, updated_at, and useful methods.
"""

from sqlalchemy.ext.declarative import declared_attr

from app.db.database import Base


class BaseModel(Base):
    """
    Base model class with common fields and methods.
    
    All models should inherit from this class to get:
    - Primary key (id)
    - Creation timestamp (created_at)
    - Update timestamp (updated_at)
    - Common utility methods
    """
    
    __abstract__ = True
    
    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name."""
        # Convert CamelCase to snake_case
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
