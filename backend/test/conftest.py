"""
Pytest configuration and fixtures for AITranslator tests.

This module provides shared fixtures and configuration for pytest tests.
"""

import pytest
from typing import Generator

# Ensure the backend directory is in the Python path
import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


@pytest.fixture
def app():
    """
    Create and configure a test application instance.

    Yields:
        Flask application configured for testing
    """
    # Import here to avoid issues with module loading order
    from app import create_app

    app = create_app({
        'TESTING': True,
        'DEBUG': True,
        'JSON_AS_ASCII': False
    })

    yield app


@pytest.fixture
def client(app):
    """
    Create a test client for the application.

    Args:
        app: Flask application fixture

    Yields:
        Flask test client
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Create a test CLI runner for the application.

    Args:
        app: Flask application fixture

    Yields:
        Flask test CLI runner
    """
    return app.test_cli_runner()


@pytest.fixture
def sample_chinese_text():
    """
    Provide sample Chinese text for testing.

    Yields:
        Sample Chinese text string
    """
    return "你好世界"


@pytest.fixture
def sample_translation_response():
    """
    Provide sample translation response data.

    Yields:
        Dictionary with sample translation response
    """
    return {
        'translation': 'Hello World',
        'keywords': ['hello', 'world']
    }


@pytest.fixture
def mock_llm_response(monkeypatch):
    """
    Mock the LLM service response.

    Args:
        monkeypatch: pytest monkeypatch fixture
    """
    from unittest.mock import MagicMock

    mock_response = MagicMock()
    mock_response.content = '''{
        "translation": "Hello World",
        "keywords": ["hello", "world"]
    }'''

    mock_model = MagicMock()
    mock_model.invoke.return_value = mock_response

    mock_llm_service = MagicMock()
    mock_llm_service.generate.return_value = mock_response.content
    mock_llm_service.generate_with_json_output.return_value = {
        'translation': 'Hello World',
        'keywords': ['hello', 'world']
    }

    monkeypatch.setattr(
        'app.services.translation_service.LLMService',
        lambda: mock_llm_service
    )

    return mock_llm_service
