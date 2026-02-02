"""
Service layer tests for AITranslator.

This module contains tests for the service layer, including
TranslationService and LLMService, with proper mocking.
"""

import pytest
from unittest.mock import MagicMock, patch, Mock

from app.services.llm_service import LLMService
from app.services.translation_service import TranslationService
from app.core import LLMServiceError, InternalError, setup_logger

logger = setup_logger(__name__)


class TestLLMService:
    """Test LLMService functionality."""

    def test_llm_service_initialization(self):
        """Test LLMService initializes correctly."""
        with patch('app.services.llm_service.ChatTongyi') as mock_chat:
            mock_model = Mock()
            mock_chat.return_value = mock_model

            service = LLMService()

            assert service.model is not None
            mock_chat.assert_called_once()

    def test_llm_service_generate_success(self):
        """Test LLMService generates response successfully."""
        mock_response = Mock()
        mock_response.content = "Test response"

        with patch('app.services.llm_service.ChatTongyi') as mock_chat:
            mock_model = Mock()
            mock_model.invoke.return_value = mock_response
            mock_chat.return_value = mock_model

            service = LLMService()
            result = service.generate("Test prompt")

            assert result == "Test response"

    def test_llm_service_generate_with_system_prompt(self):
        """Test LLMService generates response with system prompt."""
        mock_response = Mock()
        mock_response.content = "Test response"

        with patch('app.services.llm_service.ChatTongyi') as mock_chat:
            mock_model = Mock()
            mock_model.invoke.return_value = mock_response
            mock_chat.return_value = mock_model

            service = LLMService()
            result = service.generate(
                "Test prompt",
                system_prompt="You are a helpful assistant"
            )

            assert result == "Test response"
            # Verify system prompt was included
            mock_model.invoke.assert_called_once()
            args, _ = mock_model.invoke.call_args
            # Check that 2 messages were passed (system + human)
            assert len(args[0]) == 2

    def test_llm_service_generate_json_success(self):
        """Test LLMService generates JSON response successfully."""
        mock_response = Mock()
        mock_response.content = '{"key": "value"}'

        with patch('app.services.llm_service.ChatTongyi') as mock_chat:
            mock_model = Mock()
            mock_model.invoke.return_value = mock_response
            mock_chat.return_value = mock_model

            service = LLMService()
            result = service.generate_with_json_output("Test prompt")

            assert result == {"key": "value"}

    def test_llm_service_generate_json_with_extra_text(self):
        """Test LLMService extracts JSON from response with extra text."""
        mock_response = Mock()
        mock_response.content = 'Here is the JSON: {"key": "value"} and some text'

        with patch('app.services.llm_service.ChatTongyi') as mock_chat:
            mock_model = Mock()
            mock_model.invoke.return_value = mock_response
            mock_chat.return_value = mock_model

            service = LLMService()
            result = service.generate_with_json_output("Test prompt")

            assert result == {"key": "value"}

    def test_llm_service_generate_failure(self):
        """Test LLMService handles generation failure."""
        with patch('app.services.llm_service.ChatTongyi') as mock_chat:
            mock_model = Mock()
            mock_model.invoke.side_effect = Exception("API error")
            mock_chat.return_value = mock_model

            service = LLMService()

            with pytest.raises(LLMServiceError):
                service.generate("Test prompt")

    def test_llm_service_generate_json_parse_failure(self):
        """Test LLMService handles JSON parse failure."""
        mock_response = Mock()
        mock_response.content = "Not valid JSON"

        with patch('app.services.llm_service.ChatTongyi') as mock_chat:
            mock_model = Mock()
            mock_model.invoke.return_value = mock_response
            mock_chat.return_value = mock_model

            service = LLMService()

            with pytest.raises(LLMServiceError):
                service.generate_with_json_output("Test prompt")

    def test_llm_service_import_failure(self):
        """Test LLMService handles import failure."""
        with patch('app.services.llm_service.ChatTongyi', side_effect=ImportError("No module")):

            with pytest.raises(LLMServiceError) as exc_info:
                LLMService()

            assert exc_info.value.provider == "qwen"

    def test_llm_service_with_custom_model(self):
        """Test LLMService with custom model injection."""
        custom_model = Mock()
        service = LLMService(model=custom_model)

        assert service.model == custom_model


class TestTranslationService:
    """Test TranslationService functionality."""

    def test_translation_service_initialization(self):
        """Test TranslationService initializes correctly."""
        mock_llm_service = Mock()

        service = TranslationService(llm_service=mock_llm_service)

        assert service.llm_service == mock_llm_service

    def test_translation_service_translate_success(self):
        """Test successful translation."""
        mock_llm_service = Mock()
        mock_llm_service.generate_with_json_output.return_value = {
            'translation': 'Hello World',
            'keywords': ['hello', 'world']
        }

        service = TranslationService(llm_service=mock_llm_service)
        translation, keywords = service.translate('你好世界')

        assert translation == 'Hello World'
        assert keywords == ['hello', 'world']
        mock_llm_service.generate_with_json_output.assert_called_once()

    def test_translation_service_empty_text(self):
        """Test translation with empty text."""
        mock_llm_service = Mock()

        service = TranslationService(llm_service=mock_llm_service)

        with pytest.raises(InternalError):
            service.translate('')

    def test_translation_service_whitespace_only(self):
        """Test translation with whitespace-only text."""
        mock_llm_service = Mock()

        service = TranslationService(llm_service=mock_llm_service)

        with pytest.raises(InternalError):
            service.translate('   ')

    def test_translation_service_llm_failure(self):
        """Test translation when LLM service fails."""
        mock_llm_service = Mock()
        mock_llm_service.generate_with_json_output.side_effect = Exception("LLM error")

        service = TranslationService(llm_service=mock_llm_service)

        with pytest.raises(InternalError):
            service.translate('你好世界')

    def test_translation_service_empty_translation_fallback(self):
        """Test translation when LLM returns empty translation."""
        mock_llm_service = Mock()
        mock_llm_service.generate_with_json_output.return_value = {
            'translation': '',
            'keywords': ['hello', 'world']
        }

        service = TranslationService(llm_service=mock_llm_service)
        translation, keywords = service.translate('你好世界')

        assert translation == '[Translation unavailable for: 你好世界...]'
        assert keywords == ['hello', 'world']

    def test_translation_service_empty_keywords_fallback(self):
        """Test translation when LLM returns empty keywords."""
        mock_llm_service = Mock()
        mock_llm_service.generate_with_json_output.return_value = {
            'translation': 'Hello World',
            'keywords': []
        }

        service = TranslationService(llm_service=mock_llm_service)
        translation, keywords = service.translate('你好世界 hello world')

        assert translation == 'Hello World'
        # Should extract keywords from translation
        assert isinstance(keywords, list)
        assert len(keywords) > 0

    def test_translation_service_keyword_cleanup(self):
        """Test translation cleans up keywords properly."""
        mock_llm_service = Mock()
        mock_llm_service.generate_with_json_output.return_value = {
            'translation': 'Hello World',
            'keywords': [' hello ', 'world', '', '  ']
        }

        service = TranslationService(llm_service=mock_llm_service)
        translation, keywords = service.translate('你好世界')

        assert translation == 'Hello World'
        # Empty and whitespace-only keywords should be removed
        assert '' not in keywords
        assert '  ' not in keywords
        # Keywords should be lowercase
        assert all(k == k.lower() for k in keywords)

    def test_translation_service_keyword_deduplication(self):
        """Test translation removes duplicate keywords."""
        mock_llm_service = Mock()
        mock_llm_service.generate_with_json_output.return_value = {
            'translation': 'Hello World',
            'keywords': ['hello', 'world', 'hello', 'hello']
        }

        service = TranslationService(llm_service=mock_llm_service)
        translation, keywords = service.translate('你好世界')

        assert translation == 'Hello World'
        # Duplicates should be removed
        assert keywords.count('hello') == 1

    def test_translation_service_batch_translate(self):
        """Test batch translation."""
        mock_llm_service = Mock()
        mock_llm_service.generate_with_json_output.return_value = {
            'translation': 'Hello World',
            'keywords': ['hello', 'world']
        }

        service = TranslationService(llm_service=mock_llm_service)
        texts = ['你好', '世界']
        results = service.batch_translate(texts)

        assert len(results) == 2
        assert all(len(result) == 2 for result in results)

    def test_translation_service_batch_with_failure(self):
        """Test batch translation handles individual failures."""
        mock_llm_service = Mock()
        mock_llm_service.generate_with_json_output.side_effect = [
            {'translation': 'Hello', 'keywords': ['hello']},
            Exception("LLM error")
        ]

        service = TranslationService(llm_service=mock_llm_service)
        texts = ['你好', '世界']
        results = service.batch_translate(texts)

        assert len(results) == 2
        assert results[0][0] == 'Hello'
        # Second translation should use fallback
        assert results[1][0].startswith('[Translation unavailable')

    def test_translate_prompt_template(self):
        """Test that correct prompt template is used."""
        mock_llm_service = Mock()
        mock_llm_service.generate_with_json_output.return_value = {
            'translation': 'Hello World',
            'keywords': ['hello']
        }

        service = TranslationService(llm_service=mock_llm_service)
        service.translate('你好世界')

        # Verify the prompt contains the text
        call_args = mock_llm_service.generate_with_json_output.call_args
        prompt = call_args[0][0]
        assert '你好世界' in prompt
        assert 'translation' in prompt.lower()
        assert 'keywords' in prompt.lower()

    def test_translate_system_prompt(self):
        """Test that correct system prompt is used."""
        mock_llm_service = Mock()
        mock_llm_service.generate_with_json_output.return_value = {
            'translation': 'Hello World',
            'keywords': ['hello']
        }

        service = TranslationService(llm_service=mock_llm_service)
        service.translate('你好世界')

        # Verify system prompt is set
        call_args = mock_llm_service.generate_with_json_output.call_args
        system_prompt = call_args[1].get('system_prompt')
        assert system_prompt is not None
        assert 'translator' in system_prompt.lower()
