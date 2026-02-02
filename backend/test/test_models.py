"""
Pydantic model tests for AITranslator.

This module contains tests for Pydantic models to ensure
proper validation and data transformation.
"""

import pytest
from pydantic import ValidationError

from app.models.request import TranslateRequest
from app.models.response import TranslateResponse, ErrorResponse, SuccessResponse


class TestTranslateRequest:
    """Test TranslateRequest model."""

    def test_valid_request(self):
        """Test creation of valid TranslateRequest."""
        request = TranslateRequest(text="你好世界")

        assert request.text == "你好世界"

    def test_text_stripping(self):
        """Test that text is properly stripped."""
        request = TranslateRequest(text="  你好世界  ")

        assert request.text == "你好世界"

    def test_min_length_validation(self):
        """Test that empty text fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            TranslateRequest(text="")

        errors = exc_info.value.errors()
        assert any('ensure this value has at least 1 characters' in str(e) for e in errors)

    def test_max_length_validation(self):
        """Test that text exceeding max length fails validation."""
        long_text = "x" * 10001

        with pytest.raises(ValidationError) as exc_info:
            TranslateRequest(text=long_text)

        errors = exc_info.value.errors()
        assert any('ensure this value has at most 10000 characters' in str(e) for e in errors)

    def test_whitespace_only_validation(self):
        """Test that whitespace-only text fails validation."""
        with pytest.raises(ValueError):
            TranslateRequest(text="   ")

    def test_type_validation(self):
        """Test that non-string text fails validation."""
        with pytest.raises(ValidationError):
            TranslateRequest(text=123)

    def test_model_dump(self):
        """Test model dumps to dictionary correctly."""
        request = TranslateRequest(text="你好世界")
        data = request.model_dump()

        assert data == {'text': '你好世界'}

    def test_model_json(self):
        """Test model serializes to JSON correctly."""
        request = TranslateRequest(text="你好世界")
        json_str = request.model_dump_json()

        assert '"text":"你好世界"' in json_str

    def test_model_schema(self):
        """Test model schema is generated correctly."""
        schema = TranslateRequest.model_json_schema()

        assert 'properties' in schema
        assert 'text' in schema['properties']
        assert schema['properties']['text']['type'] == 'string'


class TestTranslateResponse:
    """Test TranslateResponse model."""

    def test_valid_response(self):
        """Test creation of valid TranslateResponse."""
        response = TranslateResponse(
            translation="Hello World",
            keywords=["hello", "world"]
        )

        assert response.translation == "Hello World"
        assert response.keywords == ["hello", "world"]

    def test_empty_keywords_allowed(self):
        """Test that empty keywords list is allowed."""
        response = TranslateResponse(
            translation="Hello World",
            keywords=[]
        )

        assert response.keywords == []

    def test_single_keyword(self):
        """Test response with single keyword."""
        response = TranslateResponse(
            translation="Hello",
            keywords=["hello"]
        )

        assert len(response.keywords) == 1

    def test_model_dump(self):
        """Test model dumps to dictionary correctly."""
        response = TranslateResponse(
            translation="Hello World",
            keywords=["hello", "world"]
        )
        data = response.model_dump()

        assert data == {
            'translation': 'Hello World',
            'keywords': ['hello', 'world']
        }

    def test_required_fields(self):
        """Test that all fields are required."""
        with pytest.raises(ValidationError):
            TranslateResponse(translation="Hello")

        with pytest.raises(ValidationError):
            TranslateResponse(keywords=["hello"])

    def test_model_schema(self):
        """Test model schema is generated correctly."""
        schema = TranslateResponse.model_json_schema()

        assert 'properties' in schema
        assert 'translation' in schema['properties']
        assert 'keywords' in schema['properties']


class TestErrorResponse:
    """Test ErrorResponse model."""

    def test_valid_error_response(self):
        """Test creation of valid ErrorResponse."""
        response = ErrorResponse(
            error="VALIDATION_ERROR",
            message="Invalid input"
        )

        assert response.error == "VALIDATION_ERROR"
        assert response.message == "Invalid input"

    def test_error_response_with_details(self):
        """Test ErrorResponse with details."""
        response = ErrorResponse(
            error="VALIDATION_ERROR",
            message="Invalid input",
            details={"field": "text"}
        )

        assert response.details == {"field": "text"}

    def test_error_response_without_details(self):
        """Test ErrorResponse without details."""
        response = ErrorResponse(
            error="INTERNAL_ERROR",
            message="Server error"
        )

        assert response.details is None

    def test_model_dump_without_none(self):
        """Test that None values are excluded from dump."""
        response = ErrorResponse(
            error="VALIDATION_ERROR",
            message="Invalid input"
        )
        data = response.model_dump(exclude_none=True)

        assert 'details' not in data

    def test_model_dump_with_details(self):
        """Test dump with details included."""
        response = ErrorResponse(
            error="VALIDATION_ERROR",
            message="Invalid input",
            details={"field": "text"}
        )
        data = response.model_dump(exclude_none=True)

        assert data['details'] == {"field": "text"}

    def test_model_schema(self):
        """Test model schema is generated correctly."""
        schema = ErrorResponse.model_json_schema()

        assert 'properties' in schema
        assert 'error' in schema['properties']
        assert 'message' in schema['properties']
        assert 'details' in schema['properties']


class TestSuccessResponse:
    """Test SuccessResponse model."""

    def test_valid_success_response(self):
        """Test creation of valid SuccessResponse."""
        response = SuccessResponse(
            success=True,
            data={"id": 123},
            message="Operation completed"
        )

        assert response.success is True
        assert response.data == {"id": 123}
        assert response.message == "Operation completed"

    def test_default_success_field(self):
        """Test that success field defaults to True."""
        response = SuccessResponse()

        assert response.success is True

    def test_optional_fields(self):
        """Test that data and message fields are optional."""
        response = SuccessResponse()

        assert response.data is None
        assert response.message is None

    def test_data_only(self):
        """Test response with only data."""
        response = SuccessResponse(data={"key": "value"})

        assert response.data == {"key": "value"}
        assert response.message is None

    def test_message_only(self):
        """Test response with only message."""
        response = SuccessResponse(message="Success")

        assert response.message == "Success"
        assert response.data is None

    def test_complex_data(self):
        """Test response with complex nested data."""
        complex_data = {
            "user": {
                "id": 1,
                "name": "Test User",
                "roles": ["admin", "user"]
            }
        }

        response = SuccessResponse(data=complex_data)

        assert response.data == complex_data

    def test_model_dump(self):
        """Test model dumps to dictionary correctly."""
        response = SuccessResponse(
            data={"id": 123},
            message="Success"
        )
        data = response.model_dump()

        assert data == {
            'success': True,
            'data': {"id": 123},
            'message': "Success"
        }

    def test_model_dump_exclude_none(self):
        """Test that None values are excluded."""
        response = SuccessResponse()
        data = response.model_dump(exclude_none=True)

        assert 'success' in data
        assert 'data' not in data
        assert 'message' not in data

    def test_model_schema(self):
        """Test model schema is generated correctly."""
        schema = SuccessResponse.model_json_schema()

        assert 'properties' in schema
        assert 'success' in schema['properties']
        assert 'data' in schema['properties']
        assert 'message' in schema['properties']


class TestModelIntegration:
    """Test model integration scenarios."""

    def test_request_to_response_flow(self):
        """Test flow from request to response."""
        request = TranslateRequest(text="你好世界")
        response = TranslateResponse(
            translation="Hello World",
            keywords=["hello", "world"]
        )

        assert request.text == "你好世界"
        assert response.translation == "Hello World"

    def test_error_response_from_exception(self):
        """Test creating error response from exception details."""
        response = ErrorResponse(
            error="VALIDATION_ERROR",
            message="Text field is required",
            details={"field": "text", "reason": "missing"}
        )

        assert response.error == "VALIDATION_ERROR"
        assert response.details["field"] == "text"
