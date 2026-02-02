"""
Response helper functions for API endpoints.

This module provides utility functions for creating standardized
API responses, ensuring consistency across all endpoints.
"""

from typing import Any, Optional, Tuple

from flask import jsonify, Response as FlaskResponse

from app.models.response import ErrorResponse, SuccessResponse


def create_error_response(
    error: str,
    message: str,
    status_code: int = 500,
    details: Optional[dict[str, Any]] = None
) -> Tuple[FlaskResponse, int]:
    """
    Create a standardized error response.

    This helper function creates a consistent error response format
    that can be used across all API endpoints.

    Args:
        error: The error type or code
        message: Human-readable error message
        status_code: HTTP status code to return
        details: Optional additional error details

    Returns:
        Tuple of (Flask response object, status code)

    Example:
        >>> return create_error_response(
        ...     error="VALIDATION_ERROR",
        ...     message="Invalid input",
        ...     status_code=400
        ... )
    """
    error_response = ErrorResponse(
        error=error,
        message=message,
        details=details
    )
    return jsonify(error_response.model_dump(exclude_none=True)), status_code


def create_success_response(
    data: Optional[Any] = None,
    message: Optional[str] = None,
    status_code: int = 200
) -> Tuple[FlaskResponse, int]:
    """
    Create a standardized success response.

    This helper function creates a consistent success response format
    that can be used across all API endpoints.

    Args:
        data: Response data payload
        message: Optional success message
        status_code: HTTP status code to return

    Returns:
        Tuple of (Flask response object, status code)

    Example:
        >>> return create_success_response(
        ...     data={'id': 123},
        ...     message="Created successfully",
        ...     status_code=201
        ... )
    """
    success_response = SuccessResponse(
        success=True,
        data=data,
        message=message
    )
    return jsonify(success_response.model_dump(exclude_none=True)), status_code


def create_translation_response(
    translation: str,
    keywords: list[str],
    status_code: int = 200
) -> Tuple[FlaskResponse, int]:
    """
    Create a standardized translation response.

    This helper function creates the specific response format for
    the translation endpoint.

    Args:
        translation: The translated text
        keywords: List of extracted keywords
        status_code: HTTP status code to return

    Returns:
        Tuple of (Flask response object, status code)

    Example:
        >>> return create_translation_response(
        ...     translation="Hello World",
        ...     keywords=["hello", "world"]
        ... )
    """
    response_data = {
        'translation': translation,
        'keywords': keywords
    }
    return jsonify(response_data), status_code
