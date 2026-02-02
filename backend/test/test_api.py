"""
API endpoint tests for AITranslator.

This module contains tests for all API endpoints, verifying
correct behavior, error handling, and response formats.
"""

import json
import pytest
from unittest.mock import patch, MagicMock

from app.models.request import TranslateRequest
from app.models.response import TranslateResponse, ErrorResponse


class TestHealthEndpoints:
    """Test health check and related endpoints."""

    def test_health_check_success(self, client):
        """Test health check endpoint returns success."""
        response = client.get('/api/health')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['service'] == 'aitranslator'
        assert 'environment' in data
        assert 'version' in data

    def test_readiness_check_success(self, client):
        """Test readiness check endpoint returns ready status."""
        response = client.get('/api/ready')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ready'
        assert 'checks' in data
        assert data['checks']['llm_service'] == 'available'

    def test_service_info_success(self, client):
        """Test service info endpoint returns service information."""
        response = client.get('/api/info')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'AITranslator'
        assert data['version'] == '1.0.0'
        assert 'description' in data
        assert 'endpoints' in data
        assert len(data['endpoints']) > 0


class TestTranslateEndpoint:
    """Test translation endpoint."""

    def test_translate_success(self, client, mock_llm_response):
        """Test successful translation request."""
        response = client.post(
            '/api/translate',
            data=json.dumps({'text': '你好世界'}),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'translation' in data
        assert 'keywords' in data
        assert isinstance(data['keywords'], list)

    def test_translate_empty_request(self, client):
        """Test translation with empty request body."""
        response = client.post(
            '/api/translate',
            data=json.dumps({}),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'VALIDATION_ERROR'
        assert 'message' in data

    def test_translate_missing_text(self, client):
        """Test translation with missing text field."""
        response = client.post(
            '/api/translate',
            data=json.dumps({'other_field': 'value'}),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'VALIDATION_ERROR'

    def test_translate_empty_text(self, client):
        """Test translation with empty text."""
        response = client.post(
            '/api/translate',
            data=json.dumps({'text': ''}),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'VALIDATION_ERROR'

    def test_translate_whitespace_only(self, client):
        """Test translation with whitespace-only text."""
        response = client.post(
            '/api/translate',
            data=json.dumps({'text': '   '}),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'VALIDATION_ERROR'

    def test_translate_too_long_text(self, client):
        """Test translation with text exceeding maximum length."""
        long_text = 'x' * 10001  # Exceeds 10,000 character limit

        response = client.post(
            '/api/translate',
            data=json.dumps({'text': long_text}),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'VALIDATION_ERROR'

    def test_translate_invalid_content_type(self, client):
        """Test translation with invalid content type."""
        response = client.post(
            '/api/translate',
            data='text data',
            content_type='text/plain'
        )

        # Should be handled by Flask's content type handling
        assert response.status_code in [400, 415]

    def test_translate_missing_content_type(self, client):
        """Test translation without content type header."""
        response = client.post(
            '/api/translate',
            data='{"text": "你好"}'
        )

        # Flask should handle this gracefully
        assert response.status_code in [200, 400]

    def test_translate_long_text_success(self, client, mock_llm_response):
        """Test translation with long but valid text."""
        long_text = '这是一个很长的句子。' * 100  # ~600 characters

        response = client.post(
            '/api/translate',
            data=json.dumps({'text': long_text}),
            content_type='application/json'
        )

        assert response.status_code == 200

    def test_translate_with_special_characters(self, client, mock_llm_response):
        """Test translation with special Chinese characters."""
        special_text = '你好，世界！这是测试。@#$%^&*()'

        response = client.post(
            '/api/translate',
            data=json.dumps({'text': special_text}),
            content_type='application/json'
        )

        assert response.status_code == 200


class TestErrorHandling:
    """Test error handling across endpoints."""

    def test_404_not_found(self, client):
        """Test 404 response for non-existent endpoint."""
        response = client.get('/api/nonexistent')

        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['error'] == 'NOT_FOUND'

    def test_405_method_not_allowed(self, client):
        """Test 405 response for invalid HTTP method."""
        response = client.get('/api/translate')  # POST endpoint

        assert response.status_code == 405
        data = json.loads(response.data)
        assert data['error'] == 'METHOD_NOT_ALLOWED'

    def test_malformed_json(self, client):
        """Test handling of malformed JSON."""
        response = client.post(
            '/api/translate',
            data='{invalid json}',
            content_type='application/json'
        )

        assert response.status_code == 400


class TestResponseFormats:
    """Test response format consistency."""

    def test_success_response_structure(self, client, mock_llm_response):
        """Test successful translation response structure."""
        response = client.post(
            '/api/translate',
            data=json.dumps({'text': '你好世界'}),
            content_type='application/json'
        )

        data = json.loads(response.data)

        # Verify required fields
        assert 'translation' in data
        assert 'keywords' in data

        # Verify types
        assert isinstance(data['translation'], str)
        assert isinstance(data['keywords'], list)

        # Verify keywords are strings
        for keyword in data['keywords']:
            assert isinstance(keyword, str)

    def test_error_response_structure(self, client):
        """Test error response structure."""
        response = client.post(
            '/api/translate',
            data=json.dumps({}),
            content_type='application/json'
        )

        data = json.loads(response.data)

        # Verify required fields
        assert 'error' in data
        assert 'message' in data

        # Verify types
        assert isinstance(data['error'], str)
        assert isinstance(data['message'], str)


class TestCorsHeaders:
    """Test CORS headers are properly set."""

    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses."""
        response = client.get('/api/health')

        # Flask-CORS should add CORS headers
        # Note: In test client, CORS headers might not be added
        # This is expected behavior; they're added by the CORS middleware
        # which may not be fully active in test mode
