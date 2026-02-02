"""
Data models for AITranslator.

This module contains Pydantic models for request/response validation,
ensuring type safety and proper data structure throughout the application.
"""

from .request import TranslateRequest
from .response import (
    TranslateResponse,
    ErrorResponse,
    SuccessResponse
)

__all__ = [
    'TranslateRequest',
    'TranslateResponse',
    'ErrorResponse',
    'SuccessResponse'
]
