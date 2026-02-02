"""
Translation API routes.

This module contains the translation endpoint handlers.
"""

from typing import Any

from flask import Blueprint, request
from pydantic import ValidationError

from app.api import api_bp
from app.core import (
    ValidationError as CoreValidationError,
    InternalError,
    setup_logger,
    create_error_response,
    create_translation_response
)
from app.models.request import TranslateRequest
from app.services import TranslationService
from config import settings

logger = setup_logger(__name__)

# Create translation blueprint
translate_bp = Blueprint('translate', __name__)


@translate_bp.route('/translate', methods=['POST'])
def translate():
    """
    Translate Chinese text to English and extract keywords.

    This endpoint accepts Chinese text and returns the English
    translation along with extracted keywords.

    Request Body:
        {
            "text": "要翻译的中文内容"
        }

    Success Response (200):
        {
            "translation": "English translation",
            "keywords": ["keyword1", "keyword2"]
        }

    Error Response (400):
        {
            "error": "VALIDATION_ERROR",
            "message": "Error description"
        }

    Error Response (500):
        {
            "error": "INTERNAL_ERROR",
            "message": "Error description"
        }

    Error Response (503):
        {
            "error": "LLM_SERVICE_ERROR",
            "message": "Error description"
        }
    """
    try:
        # Parse and validate request body
        request_data: dict[str, Any] = request.get_json(force=True)

        if not request_data:
            logger.warning("Received empty request body")
            return create_error_response(
                error="VALIDATION_ERROR",
                message="Request body cannot be empty",
                status_code=400
            )

        # Validate using Pydantic model
        try:
            translate_request = TranslateRequest(**request_data)
        except ValidationError as e:
            logger.warning(f"Validation error: {e}")
            error_details = {'errors': e.errors()}
            return create_error_response(
                error="VALIDATION_ERROR",
                message="Invalid request parameters",
                status_code=400,
                details=error_details
            )

        # Get text from validated request
        text = translate_request.text

        logger.info(f"Translation request received for text length: {len(text)}")

        # Process translation
        translation_service = TranslationService()
        translation, keywords = translation_service.translate(text)

        # Return success response
        logger.info("Translation completed successfully")
        return create_translation_response(
            translation=translation,
            keywords=keywords,
            status_code=200
        )

    except CoreValidationError as e:
        # Handle validation errors from core modules
        logger.warning(f"Core validation error: {e}")
        return create_error_response(
            error=e.error_code,
            message=e.message,
            status_code=e.status_code,
            details=e.details
        )

    except InternalError as e:
        # Handle internal errors
        logger.error(f"Internal error: {e}")
        return create_error_response(
            error=e.error_code,
            message=e.message,
            status_code=e.status_code,
            details=e.details if settings.app_debug else None
        )

    except Exception as e:
        # Handle unexpected errors
        logger.exception(f"Unexpected error in translate endpoint: {e}")
        return create_error_response(
            error="INTERNAL_ERROR",
            message="An unexpected error occurred",
            status_code=500
        )


# Register blueprint with API blueprint
api_bp.register_blueprint(translate_bp)
