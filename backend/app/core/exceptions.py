"""
Custom exception classes for AITranslator.

This module defines a hierarchy of custom exceptions that can be caught
and handled appropriately by the application's error handlers.
"""

from typing import Any, Optional


class AITranslatorError(Exception):
    """
    Base exception class for all AITranslator errors.

    All custom exceptions in the application should inherit from this class
    to ensure consistent error handling and response formatting.

    Attributes:
        message: Human-readable error message.
        error_code: Machine-readable error code for programmatic handling.
        details: Additional error details for debugging.
        status_code: HTTP status code to return for this error.

    Example:
        >>> raise AITranslatorError(
        ...     message="An error occurred",
        ...     error_code="GENERIC_ERROR",
        ...     status_code=500
        ... )
    """

    def __init__(
        self,
        message: str,
        error_code: str = "GENERIC_ERROR",
        details: Optional[dict[str, Any]] = None,
        status_code: int = 500
    ):
        """
        Initialize the exception.

        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
            details: Additional error details
            status_code: HTTP status code
        """
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.status_code = status_code
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the exception to a dictionary for JSON response.

        Returns:
            Dictionary representation of the error
        """
        return {
            'error': self.error_code,
            'message': self.message,
            'details': self.details if self.details else None
        }


class ValidationError(AITranslatorError):
    """
    Exception raised for request validation errors.

    This exception is used when incoming request data fails validation,
    such as missing required fields or invalid data types.

    Attributes:
        field: The field that failed validation (if applicable).
    """

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        details: Optional[dict[str, Any]] = None
    ):
        """
        Initialize the validation error.

        Args:
            message: Human-readable error message
            field: The field that caused validation failure
            details: Additional error details
        """
        error_details = details or {}
        if field:
            error_details['field'] = field

        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details=error_details,
            status_code=400
        )
        self.field = field


class LLMServiceError(AITranslatorError):
    """
    Exception raised for LLM service errors.

    This exception is used when the external LLM service (Qwen)
    encounters an error or is unavailable.

    Attributes:
        provider: The LLM provider name.
        original_error: The original exception if available.
    """

    def __init__(
        self,
        message: str,
        provider: str = "qwen",
        original_error: Optional[Exception] = None,
        details: Optional[dict[str, Any]] = None
    ):
        """
        Initialize the LLM service error.

        Args:
            message: Human-readable error message
            provider: The LLM provider name
            original_error: The original exception
            details: Additional error details
        """
        error_details = details or {}
        error_details['provider'] = provider
        if original_error:
            error_details['original_error'] = str(original_error)

        super().__init__(
            message=message,
            error_code="LLM_SERVICE_ERROR",
            details=error_details,
            status_code=503
        )
        self.provider = provider
        self.original_error = original_error


class InternalError(AITranslatorError):
    """
    Exception raised for unexpected internal errors.

    This exception is used for errors that occur within the application
    that are not related to validation or external services.

    Attributes:
        original_error: The original exception if available.
    """

    def __init__(
        self,
        message: str = "An internal server error occurred",
        original_error: Optional[Exception] = None,
        details: Optional[dict[str, Any]] = None
    ):
        """
        Initialize the internal error.

        Args:
            message: Human-readable error message
            original_error: The original exception
            details: Additional error details
        """
        error_details = details or {}
        if original_error:
            error_details['original_error'] = str(original_error)

        super().__init__(
            message=message,
            error_code="INTERNAL_ERROR",
            details=error_details,
            status_code=500
        )
        self.original_error = original_error
