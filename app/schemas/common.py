"""
Common Pydantic schema base classes.

This module provides basic Pydantic model configurations.
"""

from datetime import datetime
from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Base schema with common Pydantic configuration."""
    
    class Config:
        from_attributes = True