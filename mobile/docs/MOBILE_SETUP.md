# Flutter移动端应用 - 安装和使用指南

## 概述

这是AITranslator项目的Flutter移动端实现，提供与Web端相同的设计风格和功能。

## 项目结构

```
mobile/
├── lib/
│   ├── main.dart                      # 应用入口和主题配置
│   ├── screens/
│   │   └── home_screen.dart          # 主屏幕（输入输出界面）
│   ├── widgets/
│   │   ├── input_section.dart        # 输入框区域
│   │   ├── output_section.dart       # 输出结果区域
│   │   └── glassmorphism_container.dart  # 通用Glassmorphism组件
│   ├── providers/
│   │   └── translation_provider.dart # 状态管理
│   ├── services/
│   │   └── api_service.dart          # API通信
│   ├── models/
│   │   └── translation_result.dart   # 数据模型
│   └── theme/
│       └── app_colors.dart           # 颜色常量
├── android/                          # Android原生配置
├── ios/                              # iOS原生配置
├── pubspec.yaml                      # 项目依赖配置
└── README.md
```

## 技术栈

| 技术 | 用途 |
|-----|------|
| **Flutter 3.0+** | 跨平台UI框架 |
| **Provider** | 状态管理 |
| **HTTP** | API请求 |
| **Dart** | 编程语言 |

## 功能特性

✅ **中英翻译**
- 输入中文，获取英文翻译
- 调用后端API（默认地址：http://localhost:5001/translate）

✅ **关键词提取**
- 自动识别文本中的关键词
- 以标签形式展示

✅ **Glassmorphism UI设计**
- 磨砂玻璃效果
- 与Web端保持视觉一致

✅ **流畅动画**
- 加载状态动画
- 内容过渡动画

✅ **便捷操作**
- 一键复制翻译结果
- 字数统计
- 实时反馈

## 前提条件

### 系统要求

- **macOS**: Xcode 13.0+ (for iOS development)
- **Windows/Linux**: Android SDK (for Android development)
- **Flutter SDK**: 3.0.0 或更高版本

### 验证环境

```bash
# 检查Flutter和Dart版本
flutter --version

# 检查开发环境
flutter doctor
```

## 安装步骤

### 1. 获取代码

项目已在以下路径：
```
/Users/eversse/Documents/codes/VibeCoding/AITranslator/mobile
```

### 2. 安装依赖

```bash
cd /Users/eversse/Documents/codes/VibeCoding/AITranslator/mobile
flutter pub get
```

### 3. 后端服务验证

确保后端服务运行在 `http://localhost:5001`：

```bash
# 在backend目录
cd backend
python -m pip install -r requirements.txt
flask run --port 5001
```

## 开发和运行

### 查看可用设备

```bash
flutter devices
```

### iOS开发

#### 前提条件
- Xcode 13.0+
- iOS 11.0+

#### 获取iOS依赖
```bash
cd ios
pod install
cd ..
```

#### 运行到iOS模拟器
```bash
flutter run -d "iPhone 14"  # 使用特定模拟器
# 或直接运行（自动选择首个可用设备）
flutter run
```

#### 运行到iOS真实设备
```bash
flutter run -d <设备ID>
```

### Android开发

#### 前提条件
- Android SDK API level 21+
- Android Studio 或 Android 命令行工具

#### 运行到Android模拟器
```bash
flutter run -d emulator-5554
```

#### 运行到Android真实设备
1. 连接设备并启用USB调试
2. 确认设备被识别：
   ```bash
   adb devices
   ```
3. 运行应用：
   ```bash
   flutter run
   ```

### Web调试（可选）

```bash
flutter run -d chrome
```

## API配置

### 默认配置

API基础URL在 `lib/services/api_service.dart` 中定义：

```dart
static const String baseUrl = 'http://localhost:5001';
```

### 修改API地址

如需连接到不同的服务器，编辑 `api_service.dart`：

```dart
// 改为你的服务器地址
static const String baseUrl = 'http://your-server:port';
```

### API端点

- **POST** `/translate` 
  - 请求体: `{"text": "中文文本"}`
  - 响应: `{"translation": "...", "keywords": [...]}`

## 构建生产版本

### 构建Android APK

```bash
# Debug版本
flutter build apk --debug

# Release版本（推荐用于分发）
flutter build apk --release

# 输出路径：build/app/outputs/flutter-apk/app-release.apk
```

### 构建iOS应用

```bash
# Debug版本
flutter build ios --debug

# Release版本
flutter build ios --release

# 构建用于分发的Archive
flutter build ios --release
```

## 代码结构说明

### main.dart
应用入口点，设置主题和路由。

### HomeScreen (screens/home_screen.dart)
主屏幕，包含：
- 装饰性背景（模糊圆形）
- 标题区域
- InputSection和OutputSection组件
- 页脚

### TranslationProvider (providers/translation_provider.dart)
使用Provider进行状态管理：
- 管理输入文本、加载状态、翻译结果
- 调用ApiService进行翻译
- 通知UI更新

### ApiService (services/api_service.dart)
处理HTTP请求：
- 发送翻译请求到后端
- 解析JSON响应
- 错误处理和超时管理

## 常见问题

### Q: 应用无法连接到后端
**A:** 检查以下内容：
1. 确保后端服务运行中：`flask run --port 5001`
2. 检查API基础URL是否正确
3. 使用正确的IP地址（如果在真实设备上运行，使用电脑IP而非localhost）

### Q: iOS构建失败
**A:** 尝试以下步骤：
```bash
cd ios
rm -rf Pods
rm Podfile.lock
pod install
cd ..
flutter run
```

### Q: 如何修改应用名称？
**A:** 
- iOS: 编辑 `ios/Runner/Info.plist` 中的 `CFBundleName`
- Android: 编辑 `android/app/src/main/AndroidManifest.xml` 中的 `android:label`

### Q: 如何在真实设备上测试？
**A:** 
1. iOS: 需要Apple Developer账户和配置签名证书
2. Android: 启用USB调试，连接设备，运行 `flutter run`

## 性能优化

### 启用Release模式运行
```bash
flutter run --release
```

### 分析性能
```bash
flutter run --profile
```

## 测试

### 运行单元测试
```bash
flutter test
```

### 运行集成测试
```bash
flutter drive --target=test_driver/app.dart
```

## 发布检查清单

- [ ] 更新 `pubspec.yaml` 中的版本号
- [ ] 更新iOS应用版本号
- [ ] 更新Android应用版本号
- [ ] 确保所有图片资源已优化
- [ ] 进行充分的功能测试
- [ ] 测试真实设备上的API连接
- [ ] 检查错误处理和用户提示

## 调试技巧

### 启用调试日志
```dart
// 在main.dart中
debugPrint('Your debug message here');
```

### 使用Flutter DevTools
```bash
flutter pub global activate devtools
flutter devtools

# 在应用运行时连接
flutter run
```

### 热重载开发
在应用运行时修改Dart代码后，按 `r` 进行热重载（无需重启应用）。

## 相关文档

- [Flutter官方文档](https://flutter.dev/docs)
- [Dart编程指南](https://dart.dev/guides)
- [Provider状态管理](https://pub.dev/packages/provider)
- [HTTP包文档](https://pub.dev/packages/http)

## 许可证

MIT License

---

**最后更新**: 2026年2月2日
