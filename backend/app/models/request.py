"""
Request models for API endpoints.

This module defines Pydantic models for validating incoming API requests,
ensuring proper data structure and type safety.
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator


class TranslateRequest(BaseModel):
    """
    Request model for the translation endpoint.

    Attributes:
        text: The Chinese text to be translated.
            Must be a non-empty string with reasonable length.

    Example:
        >>> request = TranslateRequest(text="你好世界")
        >>> request.text
        '你好世界'
    """

    text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The Chinese text to translate to English",
        examples=["你好世界", "这是一个测试句子"]
    )

    @field_validator('text')
    @classmethod
    def validate_text_content(cls, v: str) -> str:
        """
        Validate that the text contains actual content.

        Args:
            v: The text value to validate

        Returns:
            The validated and stripped text

        Raises:
            ValueError: If text is empty or contains only whitespace
        """
        stripped = v.strip()
        if not stripped:
            raise ValueError('Text cannot be empty or contain only whitespace')
        return stripped

    class Config:
        """
        Pydantic model configuration.
        """
        json_schema_extra = {
            'example': {
                'text': '你好世界'
            }
        }
