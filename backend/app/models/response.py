"""
Response models for API endpoints.

This module defines Pydantic models for standardizing API responses,
ensuring consistent structure across all endpoints.
"""

from typing import Any, List, Optional
from pydantic import BaseModel, Field


class TranslateResponse(BaseModel):
    """
    Response model for the translation endpoint.

    This model represents a successful translation response containing
    the translated text and extracted keywords.

    Attributes:
        translation: The translated English text.
        keywords: List of extracted keywords from the text.

    Example:
        >>> response = TranslateResponse(
        ...     translation="Hello World",
        ...     keywords=["hello", "world"]
        ... )
    """

    translation: str = Field(
        ...,
        description="The translated English text",
        examples=["Hello World", "This is a test sentence"]
    )
    keywords: List[str] = Field(
        ...,
        min_length=0,
        description="List of keywords extracted from the translated text",
        examples=[["hello", "world"], ["test", "sentence"]]
    )

    class Config:
        """
        Pydantic model configuration.
        """
        json_schema_extra = {
            'example': {
                'translation': 'Hello World',
                'keywords': ['hello', 'world']
            }
        }


class ErrorResponse(BaseModel):
    """
    Standard error response model.

    This model provides a consistent error response structure across all
    endpoints, including error type and descriptive message.

    Attributes:
        error: The error type or code.
        message: A human-readable error message.
        details: Optional additional error details for debugging.

    Example:
        >>> error = ErrorResponse(
        ...     error="VALIDATION_ERROR",
        ...     message="Invalid request parameter"
        ... )
    """

    error: str = Field(
        ...,
        description="Error type or code",
        examples=["VALIDATION_ERROR", "INTERNAL_ERROR", "SERVICE_UNAVAILABLE"]
    )
    message: str = Field(
        ...,
        description="Human-readable error message",
        examples=["Invalid request parameter", "Internal server error"]
    )
    details: Optional[dict[str, Any]] = Field(
        default=None,
        description="Additional error details for debugging"
    )

    class Config:
        """
        Pydantic model configuration.
        """
        json_schema_extra = {
            'example': {
                'error': 'VALIDATION_ERROR',
                'message': 'Invalid request parameter'
            }
        }


class SuccessResponse(BaseModel):
    """
    Generic success response wrapper.

    This model provides a consistent success response structure that can
    wrap any data payload.

    Attributes:
        success: Always True for successful responses.
        data: The response data payload.
        message: Optional success message.

    Example:
        >>> response = SuccessResponse(
        ...     data={'id': 123},
        ...     message="Operation completed successfully"
        ... )
    """

    success: bool = Field(
        default=True,
        description="Indicates whether the request was successful"
    )
    data: Optional[Any] = Field(
        default=None,
        description="Response data payload"
    )
    message: Optional[str] = Field(
        default=None,
        description="Success message"
    )

    class Config:
        """
        Pydantic model configuration.
        """
        json_schema_extra = {
            'example': {
                'success': True,
                'data': {'id': 123},
                'message': 'Operation completed successfully'
            }
        }
