# AITranslator API Documentation

## Overview

AITranslator is an AI-powered translation service that provides Chinese-to-English translation with keyword extraction. The service uses LangChain framework integrated with Qwen (Tongyi Qianwen) LLM model.

**Base URL:** `http://localhost:5000`

**Version:** 1.0.0

## Table of Contents

- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
  - [Health Check](#health-check)
  - [Readiness Check](#readiness-check)
  - [Service Info](#service-info)
  - [Translate](#translate)
- [Error Codes](#error-codes)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)

## Authentication

Currently, the API does not require authentication. This may change in future versions.

## API Endpoints

### Health Check

Check the health status of the service.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "service": "aitranslator",
  "environment": "development",
  "version": "1.0.0"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

### Readiness Check

Check if the service is ready to accept requests.

**Endpoint:** `GET /api/ready`

**Response (Ready):**
```json
{
  "status": "ready",
  "checks": {
    "llm_service": "available"
  }
}
```

**Response (Not Ready):**
```json
{
  "status": "not_ready",
  "checks": {
    "llm_service": "unavailable"
  }
}
```

**Status Codes:**
- `200 OK` - Service is ready
- `503 Service Unavailable` - Service is not ready

---

### Service Info

Get information about the service and available endpoints.

**Endpoint:** `GET /api/info`

**Response:**
```json
{
  "name": "AITranslator",
  "version": "1.0.0",
  "description": "AI-powered Chinese to English translation service",
  "environment": "development",
  "endpoints": [
    {
      "path": "/api/translate",
      "method": "POST",
      "description": "Translate Chinese text to English"
    }
  ]
}
```

**Status Codes:**
- `200 OK` - Information retrieved successfully

---

### Translate

Translate Chinese text to English and extract keywords.

**Endpoint:** `POST /api/translate`

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "text": "要翻译的中文内容"
}
```

**Parameters:**

| Parameter | Type   | Required | Description                          | Constraints      |
|-----------|--------|----------|--------------------------------------|------------------|
| text      | string | Yes      | The Chinese text to translate        | 1-10,000 characters |

**Success Response:**
```json
{
  "translation": "The translated English text",
  "keywords": ["keyword1", "keyword2", "keyword3"]
}
```

**Status Codes:**
- `200 OK` - Translation completed successfully

**Error Response (Validation Error - 400):**
```json
{
  "error": "VALIDATION_ERROR",
  "message": "Invalid request parameters",
  "details": {
    "errors": [
      {
        "loc": ["text"],
        "msg": "ensure this value has at least 1 characters",
        "type": "value_error.any_str.min_length"
      }
    ]
  }
}
```

**Error Response (Internal Error - 500):**
```json
{
  "error": "INTERNAL_ERROR",
  "message": "An internal server error occurred"
}
```

**Error Response (LLM Service Error - 503):**
```json
{
  "error": "LLM_SERVICE_ERROR",
  "message": "Failed to generate response from LLM",
  "details": {
    "provider": "qwen",
    "original_error": "API connection timeout"
  }
}
```

**Status Codes:**
- `400 Bad Request` - Invalid request parameters
- `500 Internal Server Error` - Unexpected server error
- `503 Service Unavailable` - LLM service unavailable

## Error Codes

| Error Code           | Status Code | Description                              |
|----------------------|-------------|------------------------------------------|
| VALIDATION_ERROR     | 400         | Request validation failed                |
| BAD_REQUEST          | 400         | Malformed request                        |
| NOT_FOUND            | 404         | Resource not found                       |
| METHOD_NOT_ALLOWED   | 405         | HTTP method not allowed for this endpoint|
| INTERNAL_ERROR       | 500         | Internal server error                   |
| LLM_SERVICE_ERROR    | 503         | LLM service unavailable or error         |

## Rate Limiting

Rate limiting can be enabled via configuration. When enabled:

- **Default limit:** 60 requests per minute per IP address
- **Rate limit headers:** `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

To enable rate limiting, set `RATE_LIMIT_ENABLED=true` in your environment configuration.

## Examples

### cURL

```bash
# Health check
curl http://localhost:5000/api/health

# Translate text
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "你好世界"}'
```

### Python (requests)

```python
import requests

# Health check
response = requests.get('http://localhost:5000/api/health')
print(response.json())

# Translate text
response = requests.post(
    'http://localhost:5000/api/translate',
    json={'text': '你好世界'}
)
print(response.json())
```

### JavaScript (fetch)

```javascript
// Translate text
fetch('http://localhost:5000/api/translate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: '你好世界'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## Notes

1. **Response Time:** The translation API aims to respond within 5 seconds.
2. **Text Length:** Maximum supported text length is 10,000 characters.
3. **Keywords:** The API returns 3-5 keywords per translation.
4. **Encoding:** All responses use UTF-8 encoding.
5. **CORS:** Cross-Origin Resource Sharing is enabled for all endpoints.

## Support

For issues or questions, please refer to the project repository or contact the development team.
