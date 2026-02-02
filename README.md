# AITranslator

English | [中文](README.zh-CN.md)

AI-powered Chinese to English translation application with keyword extraction capabilities.

## Features

- **AI-Powered Translation**: Accurate Chinese to English translation using advanced LLM models
- **Keyword Extraction**: Automatically extracts 3-5 relevant keywords from translated text
- **Modern UI**: Beautiful, responsive interface built with React and Tailwind CSS
- **RESTful API**: Well-documented backend API built with Flask

## Tech Stack

### Backend
- **Flask**: Web framework
- **LangChain**: LLM integration framework
- **Pydantic**: Data validation and settings management
- **Tongyi Qianwen (Qwen)**: LLM provider

### Frontend
- **React**: UI framework
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Vite**: Build tool
- **Framer Motion**: Animation library

## Project Structure

```
AITranslator/
├── backend/              # Flask backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Core utilities
│   │   ├── models/      # Data models
│   │   └── services/    # Business logic
│   ├── config/          # Configuration
│   ├── docs/            # Backend documentation
│   └── test/            # Tests
├── frontend/            # React frontend
│   ├── src/
│   │   ├── App.tsx      # Main component
│   │   └── main.tsx     # Entry point
│   ├── public/          # Static assets
│   └── docs/            # Frontend documentation
└── PRD.md              # Product Requirements Document
```

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- Qwen API key (获取：https://dashscope.aliyun.com/)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file in backend directory:
```env
QWEN_API_KEY=your_api_key_here
QWEN_MODEL=qwen-turbo
APP_ENV=development
APP_DEBUG=True
```

5. Run the backend:
```bash
flask run --port 5001
```

Backend will be available at `http://localhost:5001`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

Frontend will be available at `http://localhost:5174`

## API Documentation

### Translation Endpoint

**POST** `/api/translate`

Request:
```json
{
  "text": "你好世界"
}
```

Response:
```json
{
  "translation": "Hello World",
  "keywords": ["hello", "world"]
}
```

See [backend/docs/API_DOCUMENTATION.md](backend/docs/API_DOCUMENTATION.md) for complete API documentation.

## Development

### Running Tests

Backend tests:
```bash
cd backend
pytest
```

Frontend tests:
```bash
cd frontend
npm test
```

### Code Style

The project follows standard Python (PEP 8) and TypeScript/React conventions.

## Environment Variables

### Backend

| Variable | Description | Default |
|----------|-------------|---------|
| `QWEN_API_KEY` | Qwen API key | Required |
| `QWEN_MODEL` | Qwen model name | qwen-turbo |
| `APP_ENV` | Environment | development |
| `APP_DEBUG` | Debug mode | True |
| `APP_PORT` | Server port | 5001 |
| `LLM_TEMPERATURE` | LLM temperature | 0.3 |
| `LLM_MAX_TOKENS` | Max tokens | 2000 |

## License

This project is for educational and demonstration purposes.

## Author

Created as a demonstration of AI-powered translation capabilities using modern web technologies.
