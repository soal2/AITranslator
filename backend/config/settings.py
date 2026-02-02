"""
Application settings configuration.

This module defines the application settings using Pydantic for validation
and type safety. It loads configuration from environment variables and
provides default values where appropriate.
"""

from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    This class provides type-safe configuration with validation,
    automatic environment variable loading, and sensible defaults.
    """

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )

    # Application Configuration
    app_name: str = Field(default='AITranslator', description='Application name')
    app_env: str = Field(default='development', description='Environment (development/staging/production)')
    app_debug: bool = Field(default=True, description='Debug mode flag')
    app_host: str = Field(default='0.0.0.0', description='Server host address')
    app_port: int = Field(default=5001, description='Server port')

    @field_validator('app_env')
    @classmethod
    def validate_app_env(cls, v: str) -> str:
        """Validate that environment is one of the allowed values."""
        allowed_environments = ['development', 'staging', 'production']
        if v.lower() not in allowed_environments:
            raise ValueError(f'app_env must be one of {allowed_environments}')
        return v.lower()

    # Qwen/Tongyi Qianwen API Configuration
    qwen_api_key: str = Field(
        ...,
        description='Qwen API key for authentication'
    )
    qwen_api_base: str = Field(
        default='https://dashscope.aliyuncs.com/compatible-mode/v1',
        description='Qwen API base URL'
    )
    qwen_model: str = Field(default='qwen-turbo', description='Qwen model to use')

    # LLM Configuration
    llm_temperature: float = Field(
        default=0.3,
        ge=0.0,
        le=2.0,
        description='LLM temperature for response randomness'
    )
    llm_max_tokens: int = Field(
        default=2000,
        gt=0,
        description='Maximum tokens in LLM response'
    )
    llm_timeout: int = Field(
        default=30000,
        gt=0,
        description='LLM request timeout in milliseconds'
    )

    # Rate Limiting
    rate_limit_enabled: bool = Field(
        default=False,
        description='Enable rate limiting'
    )
    rate_limit_per_minute: int = Field(
        default=60,
        gt=0,
        description='Maximum requests per minute'
    )

    # Logging Configuration
    log_level: str = Field(default='INFO', description='Logging level')
    log_format: str = Field(
        default='json',
        description='Log format (json/text)'
    )
    log_file: str = Field(default='logs/app.log', description='Log file path')

    @field_validator('log_level')
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate that log level is a valid Python logging level."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f'log_level must be one of {valid_levels}')
        return v.upper()

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.app_env == 'development'

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.app_env == 'production'


# Global settings instance
settings = Settings()
