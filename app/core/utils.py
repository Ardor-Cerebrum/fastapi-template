"""
Common utility functions and helpers.

This module provides basic utility functions for the application.
"""

import logging

from app.core.config import settings


# Logging configuration
def setup_logging() -> logging.Logger:
    """
    Set up application logging.

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(settings.PROJECT_NAME)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

    # Create formatter
    formatter = logging.Formatter(settings.LOG_FORMAT)
    console_handler.setFormatter(formatter)

    # Add handler to logger
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger


# Get application logger
logger = setup_logging()
