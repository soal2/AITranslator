# AI Translator Mobile App

Flutter实现的AI翻译移动端应用，提供中英文翻译和关键词提取功能。

## 特性

- ✨ 美观的Glassmorphism设计风格，与Web端保持一致
- 🎯 中文到英文的AI翻译
- 🔑 智能关键词提取
- 🎨 流畅的动画和过渡效果
- 📱 响应式设计，支持各种屏幕尺寸
- 🚀 快速的API集成

## 项目结构

```
lib/
├── main.dart                          # 应用入口
├── screens/
│   └── home_screen.dart              # 主屏幕
├── widgets/
│   ├── input_section.dart            # 输入部分
│   ├── output_section.dart           # 输出部分
│   └── glassmorphism_container.dart  # Glassmorphism容器组件
├── providers/
│   └── translation_provider.dart     # 翻译逻辑提供者
├── services/
│   └── api_service.dart              # API服务
├── models/
│   └── translation_result.dart       # 翻译结果模型
└── theme/
    └── app_colors.dart               # 应用颜色主题
```

## 快速开始

### 前提条件

- Flutter SDK 3.0.0 或更高
- Dart SDK
- 运行中的后端服务（在 `http://localhost:5001`）

### 安装依赖

```bash
cd mobile
flutter pub get
```

### 运行应用

```bash
# 运行到模拟器
flutter run

# 运行到真实设备
flutter run -d <device_id>

# 以Release模式运行
flutter run --release
```

## 构建

### 构建Android APK

```bash
flutter build apk --release
```

### 构建iOS应用

```bash
flutter build ios --release
```

## 使用方法

1. 在输入框中输入中文文本
2. 点击"Translate"按钮
3. 应用将调用后端API进行翻译
4. 查看翻译结果和提取的关键词
5. 点击复制按钮可复制翻译结果到剪贴板

## API配置

默认API地址为 `http://localhost:5001`。如需修改，请编辑 `lib/services/api_service.dart` 中的 `baseUrl`。

## 样式指南

应用采用以下设计原则：

- **背景色**: `#f5f5f7` (Apple Light Gray)
- **文本颜色**: Slate系列 (Primary: `#1F2937`, Secondary: `#6B7280`)
- **强调色**: Blue/Indigo/Purple渐变
- **圆角**: 32px（主容器）、12-20px（次要元素）
- **模糊效果**: Glassmorphism风格，使用backdrop filter

## 依赖包

- `provider`: 状态管理
- `http`: HTTP客户端
- `flutter_animate`: 动画框架
- `lottie`: 复杂动画支持
- `shared_preferences`: 本地存储

## 许可证

MIT License

## 联系方式

如有问题或建议，请联系开发团队。
