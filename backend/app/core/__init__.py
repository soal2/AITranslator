"""
Core utilities and base classes for AITranslator.

This module contains essential utilities including:
- Logging configuration
- Error handling
- Response helpers
"""

from .exceptions import (
    AITranslatorError,
    ValidationError,
    LLMServiceError,
    InternalError
)
from .logger import setup_logger
from .response import (
    create_error_response,
    create_success_response,
    create_translation_response
)

__all__ = [
    'AITranslatorError',
    'ValidationError',
    'LLMServiceError',
    'InternalError',
    'setup_logger',
    'create_error_response',
    'create_success_response',
    'create_translation_response'
]
