"""
LLM Service for interacting with language models.

This module provides a wrapper around LangChain for communicating
with LLM providers, designed for easy provider swapping.
"""

import json
import re
from typing import Any, Optional

from langchain.chat_models.base import BaseChatModel
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from config import settings

from app.core import LLMServiceError, setup_logger

logger = setup_logger(__name__)


class LLMService:
    """
    Service for interacting with Large Language Models.

    This class abstracts the complexity of communicating with various
    LLM providers, providing a simple interface for translation and
    keyword extraction tasks.

    The service is designed to be provider-agnostic, making it easy
    to switch between different LLM providers (Qwen, OpenAI, etc.)
    with minimal code changes.

    Attributes:
        model: The LangChain chat model instance.

    Example:
        >>> service = LLMService()
        >>> response = service.generate(
        ...     prompt="Translate this text",
        ...     system_prompt="You are a translator"
        ... )
    """

    def __init__(self, model: Optional[BaseChatModel] = None):
        """
        Initialize the LLM service.

        Args:
            model: Optional LangChain chat model. If not provided,
                   a default model will be created based on settings.

        Raises:
            LLMServiceError: If model initialization fails.
        """
        if model is None:
            self.model = self._create_default_model()
        else:
            self.model = model

        logger.info(
            f"LLM Service initialized with model: {settings.qwen_model}"
        )

    def _create_default_model(self) -> BaseChatModel:
        """
        Create the default LLM model based on settings.

        This method attempts to create a LangChain chat model using
        the configuration settings. It supports Qwen/Tongyi Qianwen
        as the default provider.

        Returns:
            A LangChain BaseChatModel instance

        Raises:
            LLMServiceError: If model creation fails.
        """
        try:
            from langchain_community.chat_models import ChatTongyi

            logger.debug(
                f"Creating ChatTongyi model with base: {settings.qwen_api_base}"
            )

            return ChatTongyi(
                dashscope_api_key=settings.qwen_api_key,
                model_name=settings.qwen_model,
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens,
                timeout=settings.llm_timeout // 1000,  # Convert to seconds
                base_url=settings.qwen_api_base
            )

        except ImportError as e:
            logger.error(f"Failed to import ChatTongyi: {e}")
            raise LLMServiceError(
                message="Failed to import required LangChain components",
                provider="qwen",
                original_error=e
            ) from e

        except Exception as e:
            logger.error(f"Failed to create LLM model: {e}")
            raise LLMServiceError(
                message="Failed to initialize LLM model",
                provider="qwen",
                original_error=e
            ) from e

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            prompt: The main user prompt
            system_prompt: Optional system prompt to set context
            **kwargs: Additional parameters to pass to the model

        Returns:
            The generated text response

        Raises:
            LLMServiceError: If the LLM request fails.

        Example:
            >>> response = llm_service.generate(
            ...     prompt="Hello",
            ...     system_prompt="You are a helpful assistant"
            ... )
        """
        try:
            messages = []

            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))

            messages.append(HumanMessage(content=prompt))

            logger.debug(f"Sending request to LLM with prompt length: {len(prompt)}")

            response = self.model.invoke(messages, **kwargs)

            logger.info(
                f"LLM request completed. Response length: {len(response.content)}"
            )

            return response.content

        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise LLMServiceError(
                message="Failed to generate response from LLM",
                provider="qwen",
                original_error=e
            ) from e

    def generate_with_json_output(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> dict[str, Any]:
        """
        Generate a response from the LLM and parse as JSON.

        This method is useful when the LLM is instructed to return
        structured JSON data.

        Args:
            prompt: The main user prompt
            system_prompt: Optional system prompt to set context
            **kwargs: Additional parameters to pass to the model

        Returns:
            The parsed JSON response as a dictionary

        Raises:
            LLMServiceError: If the LLM request fails or response
                           cannot be parsed as JSON.

        Example:
            >>> result = llm_service.generate_with_json_output(
            ...     prompt="Return JSON with translation and keywords"
            ... )
            >>> print(result['translation'])
        """
        try:
            response_text = self.generate(prompt, system_prompt, **kwargs)

            # Attempt to extract JSON from the response
            json_match = re.search(r'\{[\s\S]*\}', response_text)

            if json_match:
                json_str = json_match.group()
                logger.debug(f"Extracted JSON from response: {json_str[:100]}...")
                return json.loads(json_str)

            # Fallback: try to parse the entire response as JSON
            logger.warning("No JSON pattern found, attempting to parse entire response")
            return json.loads(response_text)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.debug(f"Response text: {response_text[:500]}")
            raise LLMServiceError(
                message="LLM response could not be parsed as JSON",
                provider="qwen",
                original_error=e,
                details={'raw_response': response_text[:500]}
            ) from e

        except Exception as e:
            logger.error(f"JSON generation failed: {e}")
            raise LLMServiceError(
                message="Failed to generate JSON response from LLM",
                provider="qwen",
                original_error=e
            ) from e
