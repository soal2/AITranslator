# 快速开始指南

## 5分钟快速上手

### 第1步：环境检查
```bash
flutter --version
flutter doctor
```
确保所有绿色勾号（✓）。

### 第2步：获取依赖
```bash
cd /Users/eversse/Documents/codes/VibeCoding/AITranslator/mobile
flutter pub get
```

### 第3步：启动后端服务
```bash
# 在另一个终端
cd /Users/eversse/Documents/codes/VibeCoding/AITranslator/backend
python -m pip install -r requirements.txt
flask run --port 5001
```

### 第4步：运行应用
```bash
flutter run
```

就这么简单！应用应该在模拟器或设备上启动。

---

## 文件说明

### 核心文件（必读）

| 文件 | 用途 | 关键点 |
|-----|------|--------|
| [main.dart](lib/main.dart) | 应用入口 | 初始化Provider、主题 |
| [home_screen.dart](lib/screens/home_screen.dart) | 主屏幕 | 布局和设计实现 |
| [translation_provider.dart](lib/providers/translation_provider.dart) | 状态管理 | 翻译逻辑 |
| [api_service.dart](lib/services/api_service.dart) | API通信 | 后端交互 |

### 组件文件

| 文件 | 职责 |
|-----|------|
| [input_section.dart](lib/widgets/input_section.dart) | 输入框UI |
| [output_section.dart](lib/widgets/output_section.dart) | 结果显示UI |
| [glassmorphism_container.dart](lib/widgets/glassmorphism_container.dart) | 可复用组件 |

### 支持文件

| 文件 | 内容 |
|-----|------|
| [translation_result.dart](lib/models/translation_result.dart) | 数据结构 |
| [app_colors.dart](lib/theme/app_colors.dart) | 颜色常量 |

---

## 项目特色

### 🎨 设计特点
- **Glassmorphism风格**: 使用BackdropFilter实现磨砂玻璃效果
- **响应式布局**: 适配各种屏幕尺寸
- **一致的配色**: 遵循Apple Human Interface Guidelines
- **平滑动画**: Flutter内置动画库实现过渡效果

### 🔌 技术亮点
- **Provider模式**: 清晰的状态管理分离
- **async/await**: 异步API调用处理
- **Custom Widgets**: 可复用的UI组件
- **Error Handling**: 完整的错误处理和用户反馈

### ⚡ 性能优化
- 使用const构造函数避免重建
- 细粒度Consumer使用
- 异步网络请求非阻塞
- 适当的内存管理

---

## 常见开发任务

### 添加新页面

1. 创建文件 `lib/screens/new_screen.dart`
2. 继承StatefulWidget或StatelessWidget
3. 在main.dart中配置路由

### 修改样式

编辑 `lib/theme/app_colors.dart` 修改颜色常量，所有引用会自动更新。

### 修改API地址

编辑 `lib/services/api_service.dart` 中的 `baseUrl`。

### 调试状态变化

在TranslationProvider中添加日志：
```dart
debugPrint('Translation result: $_result');
```

---

## 生产发布流程

### Android发布
1. 生成签名密钥
2. 配置签名信息
3. 构建APK或AAB
4. 上传到Google Play

### iOS发布
1. 配置Apple开发者账户
2. 创建证书和预配文件
3. 构建Archive
4. 上传到App Store

详细步骤见 [MOBILE_SETUP.md](../MOBILE_SETUP.md)

---

## 问题反馈

如遇到问题，请：
1. 检查 [MOBILE_SETUP.md](../MOBILE_SETUP.md) 的常见问题部分
2. 查看 `flutter doctor` 输出
3. 查看应用日志：`flutter logs`

祝开发愉快！🚀
