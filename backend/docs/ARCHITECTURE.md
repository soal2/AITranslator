# AITranslator Architecture Documentation

## System Overview

AITranslator is a microservice built on Flask that provides AI-powered Chinese-to-English translation with keyword extraction. The service uses LangChain framework to interact with Qwen (Tongyi Qianwen) LLM model.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                           Client Layer                          │
│                     (Web, Mobile, CLI)                          │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTP/REST API
┌─────────────────────────────▼───────────────────────────────────┐
│                      API Gateway Layer                          │
│                   Flask Application (app.py)                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │               Middleware & Error Handling                  │  │
│  │  • CORS                                                    │  │
│  │  • Request Logging                                         │  │
│  │  • Error Handlers                                          │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                    API Routes Layer                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐ │
│  │  translate_bp    │  │   health_bp      │  │   info_bp     │ │
│  │  /api/translate  │  │  /api/health     │  │  /api/info    │ │
│  └──────────────────┘  └──────────────────┘  └───────────────┘ │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                    Service Layer                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              TranslationService                            │  │
│  │  • Translate Chinese to English                           │  │
│  │  • Extract keywords                                       │  │
│  │  • Batch translation support                              │  │
│  └─────────────────────┬─────────────────────────────────────┘  │
│                        │                                          │
│  ┌─────────────────────▼─────────────────────────────────────┐  │
│  │                    LLMService                               │  │
│  │  • Abstract LLM provider interface                        │  │
│  │  • Qwen/Tongyi Qianwen integration                        │  │
│  │  • JSON response parsing                                  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                   External Services                             │
│              Qwen (Tongyi Qianwen) API                          │
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
backend/
├── app/                      # Application package
│   ├── __init__.py           # Application factory
│   ├── api/                  # API routes
│   │   ├── __init__.py
│   │   ├── translate_routes.py    # Translation endpoints
│   │   └── health_routes.py       # Health check endpoints
│   ├── core/                 # Core utilities
│   │   ├── __init__.py
│   │   ├── exceptions.py          # Custom exceptions
│   │   ├── logger.py              # Logging configuration
│   │   └── response.py            # Response helpers
│   ├── models/               # Data models (Pydantic)
│   │   ├── __init__.py
│   │   ├── request.py             # Request models
│   │   └── response.py            # Response models
│   └── services/             # Business logic layer
│       ├── __init__.py
│       ├── llm_service.py         # LLM abstraction layer
│       └── translation_service.py # Translation business logic
├── config/                  # Configuration
│   ├── __init__.py
│   └── settings.py              # Application settings
├── docs/                    # Documentation
│   ├── API_DOCUMENTATION.md
│   └── ARCHITECTURE.md
├── test/                    # Tests
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_services.py
│   └── test_models.py
├── logs/                    # Log files (created at runtime)
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
└── run.py                  # Application entry point
```

## Key Components

### 1. Application Factory (`app/__init__.py`)

Implements the application factory pattern for:
- Easy testing with multiple instances
- Flexible configuration
- Clean separation of concerns

**Key Functions:**
- `create_app()`: Creates and configures the Flask application
- `_configure_app()`: Sets up application configuration
- `_init_extensions()`: Initializes Flask extensions (CORS)
- `_register_blueprints()`: Registers API route blueprints
- `_register_error_handlers()`: Sets up global error handling

### 2. API Routes Layer (`app/api/`)

Handles HTTP requests and responses.

**translate_routes.py:**
- `POST /api/translate`: Main translation endpoint
- Validates input using Pydantic models
- Delegates business logic to service layer
- Standardizes error responses

**health_routes.py:**
- `GET /api/health`: Service health check
- `GET /api/ready`: Readiness probe
- `GET /api/info`: Service information

### 3. Service Layer (`app/services/`)

Contains business logic and external service integration.

**LLMService:**
- Abstracts LLM provider interactions
- Supports JSON output parsing
- Designed for easy provider swapping
- Currently implements Qwen/Tongyi Qianwen integration

**TranslationService:**
- High-level translation orchestration
- Keyword extraction
- Batch translation support
- Fallback mechanisms

### 4. Core Layer (`app/core/`)

Provides shared utilities and infrastructure.

**Exceptions:**
- `AITranslatorError`: Base exception class
- `ValidationError`: Request validation errors
- `LLMServiceError`: LLM service errors
- `InternalError`: Unexpected internal errors

**Logger:**
- Centralized logging configuration
- JSON and text format support
- Console and file handlers

**Response Helpers:**
- `create_error_response()`: Standardized error responses
- `create_success_response()`: Standardized success responses
- `create_translation_response()`: Translation-specific responses

### 5. Models Layer (`app/models/`)

Pydantic models for type safety and validation.

**Request Models:**
- `TranslateRequest`: Validates translation requests

**Response Models:**
- `TranslateResponse`: Translation response structure
- `ErrorResponse`: Standard error response
- `SuccessResponse`: Generic success response wrapper

### 6. Configuration Layer (`config/`)

Centralized configuration management using Pydantic Settings.

**Settings:**
- Type-safe environment variable loading
- Validation and defaults
- Environment-specific configuration
- Easy test configuration

## Design Patterns

### 1. Application Factory Pattern

The application factory pattern allows:
- Multiple application instances for testing
- Flexible configuration at creation time
- Clean separation between creation and configuration

### 2. Service Layer Pattern

Business logic is encapsulated in service classes:
- Controllers handle HTTP concerns only
- Services contain business logic
- Easy to test and maintain

### 3. Repository Pattern Abstraction

LLMService abstracts LLM provider:
- Easy to switch between providers
- Consistent interface for callers
- Provider-specific details hidden

### 4. Dependency Injection

Services accept dependencies via constructor:
- Easy to mock for testing
- Loose coupling between components
- Flexible composition

### 5. Exception Hierarchy

Custom exception hierarchy for:
- Specific error handling
- Consistent error responses
- Easy error categorization

## Data Flow

### Translation Request Flow

```
1. Client sends POST request to /api/translate
   ↓
2. Flask route receives request
   ↓
3. Request JSON parsed and validated
   ↓
4. TranslationService instantiated
   ↓
5. TranslationService calls LLMService
   ↓
6. LLMService sends request to Qwen API
   ↓
7. LLMService receives and parses response
   ↓
8. TranslationService processes result
   ↓
9. Response formatted and returned to client
```

### Error Handling Flow

```
1. Exception occurs at any layer
   ↓
2. Exception caught by nearest handler
   ↓
3. Exception converted to appropriate type
   ↓
4. Error response created with status code
   ↓
5. Error logged with appropriate level
   ↓
6. Error response returned to client
```

## Extensibility

### Adding New LLM Providers

To add a new LLM provider:

1. Extend `LLMService` or create a new service class
2. Implement the same interface
3. Update `_create_default_model()` method
4. Add provider-specific configuration

### Adding New Endpoints

To add new endpoints:

1. Create a new blueprint in `app/api/`
2. Define route handlers
3. Register blueprint in `app/__init__.py`
4. Update API documentation

### Adding New Services

To add new services:

1. Create service class in `app/services/`
2. Implement business logic
3. Inject dependencies via constructor
4. Add unit tests

## Security Considerations

1. **Input Validation:** All inputs validated using Pydantic models
2. **SQL Injection:** Not applicable (no SQL database)
3. **XSS Prevention:** Proper JSON encoding
4. **Rate Limiting:** Optional rate limiting available
5. **CORS:** Configurable CORS settings
6. **Error Messages:** Detailed errors only in development

## Future Enhancements

1. **Caching:** Redis-based caching for translation results
2. **Batch Processing:** Async batch translation
3. **Rate Limiting:** Distributed rate limiting with Redis
4. **Authentication:** API key or OAuth2 authentication
5. **Monitoring:** Prometheus metrics and tracing
6. **Database:** Store translation history and analytics
7. **WebSocket:** Real-time translation streaming
8. **Multi-language Support:** Support for additional language pairs
