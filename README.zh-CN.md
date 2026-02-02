# AITranslator

[English](README.md) | 中文

AI 驱动的中文到英文翻译应用，具有关键词提取功能。

## 功能特性

- **AI 驱动翻译**：使用先进的大语言模型进行准确的中英翻译
- **关键词提取**：自动从翻译文本中提取 3-5 个相关关键词
- **现代化 UI**：使用 React 和 Tailwind CSS 构建的美观、响应式界面
- **RESTful API**：完整文档化的 Flask 后端 API

## 技术栈

### 后端
- **Flask**：Web 框架
- **LangChain**：LLM 集成框架
- **Pydantic**：数据验证和设置管理
- **通义千问 (Qwen)**：LLM 提供商

### 前端
- **React**：UI 框架
- **TypeScript**：类型安全的 JavaScript
- **Tailwind CSS**：实用优先的 CSS 框架
- **Vite**：构建工具
- **Framer Motion**：动画库

## 项目结构

```
AITranslator/
├── backend/              # Flask 后端
│   ├── app/
│   │   ├── api/         # API 路由
│   │   ├── core/        # 核心工具
│   │   ├── models/      # 数据模型
│   │   └── services/    # 业务逻辑
│   ├── config/          # 配置管理
│   ├── docs/            # 后端文档
│   └── test/            # 测试
├── frontend/            # React 前端
│   ├── src/
│   │   ├── App.tsx      # 主组件
│   │   └── main.tsx     # 入口文件
│   ├── public/          # 静态资源
│   └── docs/            # 前端文档
└── PRD.md              # 产品需求文档
```

## 快速开始

### 前置条件

- Python 3.12+
- Node.js 18+
- 通义千问 API 密钥（获取：https://dashscope.aliyun.com/）

### 后端设置

1. 进入后端目录：
```bash
cd backend
```

2. 创建虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Windows 上：venv\Scripts\activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 在后端目录创建 `.env` 文件：
```env
QWEN_API_KEY=你的_api_密钥
QWEN_MODEL=qwen-turbo
APP_ENV=development
APP_DEBUG=True
```

5. 运行后端服务：
```bash
flask run --port 5001
```

后端服务将在 `http://localhost:5001` 可用

### 前端设置

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
```

3. 启动开发服务器：
```bash
npm run dev
```

前端服务将在 `http://localhost:5174` 可用

## API 文档

### 翻译端点

**POST** `/api/translate`

请求示例：
```json
{
  "text": "你好世界"
}
```

响应示例：
```json
{
  "translation": "Hello World",
  "keywords": ["hello", "world"]
}
```

完整的 API 文档请参考 [backend/docs/API_DOCUMENTATION.md](backend/docs/API_DOCUMENTATION.md)

## 开发

### 运行测试

后端测试：
```bash
cd backend
pytest
```

前端测试：
```bash
cd frontend
npm test
```

### 代码风格

本项目遵循标准的 Python (PEP 8) 和 TypeScript/React 约定。

## 环境变量

### 后端

| 变量 | 描述 | 默认值 |
|------|------|--------|
| `QWEN_API_KEY` | 通义千问 API 密钥 | 必需 |
| `QWEN_MODEL` | 通义千问模型名称 | qwen-turbo |
| `APP_ENV` | 运行环境 | development |
| `APP_DEBUG` | 调试模式 | True |
| `APP_PORT` | 服务器端口 | 5001 |
| `LLM_TEMPERATURE` | LLM 温度参数 | 0.3 |
| `LLM_MAX_TOKENS` | 最大令牌数 | 2000 |

## 获取 API 密钥

### 通义千问 API 密钥

1. 访问 https://dashscope.aliyun.com/
2. 注册或登录账户
3. 进入 API 密钥管理页面
4. 生成新的 API 密钥
5. 将密钥复制到 `.env` 文件中

## 项目特性详解

### 后端架构

- **模块化设计**：分离 API 路由、业务逻辑和数据模型
- **错误处理**：完整的异常处理和错误响应机制
- **日志记录**：支持 JSON 和文本两种日志格式
- **配置管理**：使用 Pydantic 进行类型安全的配置

### 前端特性

- **响应式设计**：适配桌面、平板和移动设备
- **实时反馈**：加载状态、复制反馈和错误提示
- **流畅动画**：使用 Framer Motion 实现精致的界面动画
- **现代样式**：采用 Apple 设计语言的美观 UI

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目用于教育和演示目的。

## 作者

本项目作为使用现代 Web 技术进行 AI 驱动翻译功能的演示而创建。

## 相关链接

- [产品需求文档](PRD.md)
- [后端 API 文档](backend/docs/API_DOCUMENTATION.md)
- [前端设计文档](frontend/docs/DESIGN.md)
