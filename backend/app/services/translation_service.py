"""
Translation service for handling text translation.

This module contains business logic for translating text using LLM
services and extracting keywords.
"""

import re
from typing import Optional

from app.core import InternalError, setup_logger
from app.services.llm_service import LLMService

logger = setup_logger(__name__)


class TranslationService:
    """
    Service for handling translation operations.

    This service provides high-level translation functionality using
    LLM services, including translation and keyword extraction.

    The service is designed to be easily extensible to support
    multiple translation providers and translation strategies.

    Attributes:
        llm_service: The LLM service instance for generating translations.

    Example:
        >>> service = TranslationService()
        >>> translation, keywords = service.translate("你好世界")
        >>> print(f"{translation}: {keywords}")
        Hello World: ['hello', 'world']
    """

    # System prompt for translation tasks
    TRANSLATION_SYSTEM_PROMPT = (
        "You are a professional Chinese-English translator. "
        "Your task is to translate Chinese text to accurate, "
        "natural-sounding English. Additionally, extract 3-5 "
        "relevant keywords from the translated text."
    )

    # Template for translation requests
    TRANSLATION_PROMPT_TEMPLATE = (
        "Translate the following Chinese text to English "
        "and extract 3-5 relevant keywords.\n\n"
        "Please return the result in the following JSON format:\n"
        "{{\n"
        '  "translation": "<translated English text>",\n'
        '  "keywords": ["<keyword1>", "<keyword2>", ...]\n'
        "}}\n\n"
        "Chinese text to translate:\n{text}"
    )

    def __init__(self, llm_service: Optional[LLMService] = None):
        """
        Initialize the translation service.

        Args:
            llm_service: Optional LLM service instance. If not provided,
                        a new instance will be created.
        """
        if llm_service is None:
            self.llm_service = LLMService()
        else:
            self.llm_service = llm_service

        logger.info("Translation Service initialized")

    def translate(self, text: str) -> tuple[str, list[str]]:
        """
        Translate Chinese text to English and extract keywords.

        This method uses the LLM service to generate a translation
        and extract relevant keywords from the text.

        Args:
            text: The Chinese text to translate

        Returns:
            A tuple containing:
                - translation: The English translation
                - keywords: List of extracted keywords

        Raises:
            InternalError: If translation fails

        Example:
            >>> service = TranslationService()
            >>> translation, keywords = service.translate("你好世界")
            >>> print(translation)
            Hello World
            >>> print(keywords)
            ['hello', 'world']
        """
        try:
            # Validate input
            if not text or not text.strip():
                raise ValueError("Text cannot be empty")

            logger.info(f"Starting translation for text length: {len(text)}")

            # Generate prompt with the input text
            prompt = self.TRANSLATION_PROMPT_TEMPLATE.format(text=text)

            # Request JSON output from LLM
            logger.debug("Sending translation request to LLM")
            result = self.llm_service.generate_with_json_output(
                prompt=prompt,
                system_prompt=self.TRANSLATION_SYSTEM_PROMPT
            )

            # Extract translation and keywords from result
            translation = result.get('translation', '').strip()
            keywords = result.get('keywords', [])

            # Validate and clean results
            if not translation:
                logger.warning("LLM returned empty translation, using fallback")
                translation = self._fallback_translate(text)

            if not keywords:
                logger.warning("LLM returned empty keywords, extracting from translation")
                keywords = self._extract_keywords_from_text(translation)

            # Clean keywords (remove empty strings and duplicates)
            keywords = [k.strip().lower() for k in keywords if k and k.strip()]
            keywords = list(dict.fromkeys(keywords))  # Remove duplicates while preserving order

            logger.info(
                f"Translation completed. "
                f"Translation length: {len(translation)}, "
                f"Keywords found: {len(keywords)}"
            )

            return translation, keywords

        except ValueError as e:
            logger.error(f"Validation error: {e}")
            raise InternalError(message=str(e)) from e

        except Exception as e:
            logger.error(f"Translation failed: {e}")
            raise InternalError(
                message=f"Failed to translate text: {str(e)}",
                original_error=e
            ) from e

    def _fallback_translate(self, text: str) -> str:
        """
        Fallback translation method.

        This is a simple fallback used when the LLM fails to provide
        a translation. In production, you might want to implement
        a more sophisticated fallback strategy.

        Args:
            text: The Chinese text

        Returns:
            A fallback translation string
        """
        logger.warning("Using fallback translation")
        return f"[Translation unavailable for: {text[:50]}...]"

    def _extract_keywords_from_text(self, text: str) -> list[str]:
        """
        Extract keywords from text using simple heuristics.

        This is a fallback method for keyword extraction when the LLM
        fails to provide keywords. It uses simple frequency-based
        extraction and common word filtering.

        Args:
            text: The text to extract keywords from

        Returns:
            List of extracted keywords
        """
        # Convert to lowercase and split into words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())

        # Remove common stop words
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can',
            'had', 'has', 'have', 'this', 'with', 'that', 'were', 'which',
            'their', 'there', 'from', 'been', 'more', 'will', 'would', 'about'
        }

        filtered_words = [w for w in words if w not in stop_words]

        # Get top 5 most frequent words
        from collections import Counter
        word_counts = Counter(filtered_words)
        keywords = [word for word, _ in word_counts.most_common(5)]

        logger.debug(f"Extracted keywords using fallback: {keywords}")
        return keywords

    def batch_translate(self, texts: list[str]) -> list[tuple[str, list[str]]]:
        """
        Translate multiple texts in batch.

        Args:
            texts: List of Chinese texts to translate

        Returns:
            List of tuples containing (translation, keywords) for each input

        Example:
            >>> service = TranslationService()
            >>> results = service.batch_translate(["你好", "世界"])
            >>> for translation, keywords in results:
            ...     print(f"{translation}: {keywords}")
        """
        results = []
        for i, text in enumerate(texts, 1):
            logger.info(f"Processing batch translation {i}/{len(texts)}")
            try:
                result = self.translate(text)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to translate text {i}: {e}")
                # Append error result to maintain list order
                results.append((self._fallback_translate(text), []))
        return results
