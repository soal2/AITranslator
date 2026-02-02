# Flutter 移动端 - 文件导航地图

## 📍 项目导航

### 🎯 快速导航

**第一次使用?** → [QUICKSTART.md](QUICKSTART.md) (5分钟快速开始)

**需要详细设置?** → [../MOBILE_SETUP.md](../MOBILE_SETUP.md) (完整安装指南)

**开发者指南?** → [DEVELOPMENT.md](DEVELOPMENT.md) (开发参考)

**项目总览?** → [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md) (详细项目说明)

---

## 📁 文件结构详解

```
mobile/
│
├── 📄 pubspec.yaml                  ← 依赖管理 [编辑这里添加新依赖]
├── 📄 README.md                     ← 项目说明
├── 📄 QUICKSTART.md                 ← ⭐ 快速开始 (新手必读)
├── 📄 DEVELOPMENT.md                ← 开发参考指南
├── 📄 COMPLETE_GUIDE.md             ← 项目完整文档
├── 📁 .gitignore                    ← Git忽略配置
│
├── 📂 lib/                          ← Dart源代码目录
│   │
│   ├── 📄 main.dart                 ← ⭐⭐⭐ 应用入口 [修改这里调整主题]
│   │
│   ├── 📂 screens/                  ← 页面屏幕
│   │   └── 📄 home_screen.dart      ← ⭐⭐ 主屏幕 [核心UI实现]
│   │
│   ├── 📂 widgets/                  ← 可复用组件
│   │   ├── 📄 input_section.dart    ← 输入框部分
│   │   ├── 📄 output_section.dart   ← 输出结果部分
│   │   └── 📄 glassmorphism_container.dart ← 玻璃效果容器
│   │
│   ├── 📂 providers/                ← 状态管理
│   │   └── 📄 translation_provider.dart ← ⭐⭐ 状态逻辑 [翻译业务逻辑]
│   │
│   ├── 📂 services/                 ← 服务层
│   │   └── 📄 api_service.dart      ← ⭐⭐ API通信 [修改API地址在这里]
│   │
│   ├── 📂 models/                   ← 数据模型
│   │   └── 📄 translation_result.dart ← 翻译结果数据结构
│   │
│   ├── 📂 config/                   ← 配置文件
│   │   ├── 📄 app_config.dart       ← 应用配置 [环境配置]
│   │   └── 📄 constants.dart        ← 常量定义
│   │
│   └── 📂 theme/                    ← 主题设置
│       └── 📄 app_colors.dart       ← ⭐ 颜色主题 [修改样式在这里]
│
├── 📂 android/                      ← Android原生配置
│   └── app/src/main/java/...        ← Android Java代码
│
├── 📂 ios/                          ← iOS原生配置
│   └── Runner/Info.plist            ← iOS应用配置
│
├── 📂 test/                         ← 测试文件
│   └── (待完善)
│
└── 📂 public/                       ← 公共资源
    └── (图片、图标等)
```

---

## 🔍 文件用途速查表

### 核心文件（必须理解）

| 文件 | 行数 | 用途 | 修改场景 |
|-----|-----|------|---------|
| [main.dart](lib/main.dart) | ~40 | 应用启动和主题 | 改主题色、改应用名 |
| [home_screen.dart](lib/screens/home_screen.dart) | ~150 | 主UI布局 | 调整布局、改样式 |
| [api_service.dart](lib/services/api_service.dart) | ~40 | API通信 | 改API地址、改请求格式 |
| [translation_provider.dart](lib/providers/translation_provider.dart) | ~35 | 状态管理 | 改业务逻辑、改状态结构 |

### UI组件文件

| 文件 | 行数 | 用途 | 特点 |
|-----|-----|------|------|
| [input_section.dart](lib/widgets/input_section.dart) | ~80 | 输入框组件 | 包含字符计数、按钮 |
| [output_section.dart](lib/widgets/output_section.dart) | ~120 | 输出组件 | 展示翻译和关键词 |
| [glassmorphism_container.dart](lib/widgets/glassmorphism_container.dart) | ~40 | 通用容器 | 可复用、支持自定义 |

### 支持文件

| 文件 | 用途 |
|-----|------|
| [translation_result.dart](lib/models/translation_result.dart) | 数据结构和序列化 |
| [app_colors.dart](lib/theme/app_colors.dart) | 颜色常量定义 |
| [app_config.dart](lib/config/app_config.dart) | API和应用配置 |
| [constants.dart](lib/config/constants.dart) | UI和API常量 |

---

## 🚀 常见操作指南

### 我想...

#### 改变应用颜色
1. 打开 [app_colors.dart](lib/theme/app_colors.dart)
2. 修改Color常量
3. 保存，热重载

#### 改变API地址
1. 打开 [api_service.dart](lib/services/api_service.dart)
2. 修改 `static const String baseUrl = '...'`
3. 或者编辑 [app_config.dart](lib/config/app_config.dart)

#### 修改动画速度
1. 打开 [app_config.dart](lib/config/app_config.dart)
2. 修改 `Duration` 常量
3. 或在具体widget中调整

#### 添加新页面
1. 在 `lib/screens/` 创建新文件
2. 继承 StatelessWidget 或 StatefulWidget
3. 在 main.dart 配置路由

#### 修改UI布局
1. 打开 [home_screen.dart](lib/screens/home_screen.dart)
2. 修改 build() 方法中的Widget树
3. 调整Padding、SizedBox等间距

#### 添加新功能
1. 如果涉及状态：修改 [translation_provider.dart](lib/providers/translation_provider.dart)
2. 如果涉及API：修改 [api_service.dart](lib/services/api_service.dart)
3. 如果涉及UI：修改对应的 widget 文件

#### 添加新依赖
1. 编辑 [pubspec.yaml](pubspec.yaml)
2. 运行 `flutter pub get`
3. 在代码中 `import` 新包

---

## 📚 代码示例

### 状态管理使用示例

```dart
// 在widget中使用Provider
Consumer<TranslationProvider>(
  builder: (context, provider, _) {
    return Text(provider.result?.translation ?? '');
  },
)
```

### API调用示例

```dart
// 直接调用
final result = await ApiService().translate('你好');

// 通过Provider调用
final provider = Provider.of<TranslationProvider>(context);
await provider.translate('你好');
```

### 自定义Widget示例

```dart
// 使用GlassmorphismContainer
GlassmorphismContainer(
  child: Text('Hello'),
  padding: EdgeInsets.all(16),
  borderRadius: 20,
)
```

---

## 🔧 开发工具命令

### 常用命令速查

```bash
# 基础命令
flutter pub get              # 获取依赖
flutter pub upgrade          # 升级依赖
flutter clean               # 清理缓存
flutter format .            # 格式化代码
flutter analyze             # 代码分析

# 运行命令
flutter run                 # 运行应用
flutter run -d <设备ID>    # 运行到特定设备
flutter run --release       # Release模式

# 构建命令
flutter build apk           # 构建Android
flutter build ios           # 构建iOS
flutter build apk --release # 构建Android Release

# 调试命令
flutter logs                # 查看日志
flutter doctor              # 检查环境
flutter packages clean      # 清理包
```

---

## 🎨 UI样式参考

### 主要颜色
- **背景**: `#f5f5f7` (浅灰)
- **文本主**: `#1f2937` (深灰)
- **文本次**: `#6b7280` (中灰)
- **强调**: `#2563EB` (蓝) → `#9333EA` (紫)

### 间距规范
- **大**: 24px
- **标准**: 16px
- **小**: 8px

### 圆角规范
- **大容器**: 32px
- **小容器**: 12px
- **按钮**: 18px

### 动画时长
- **标准**: 300ms
- **快速**: 150ms
- **缓慢**: 500ms

---

## 📊 数据流向图

```
用户界面 (Widget)
    ↓
点击事件 (onPressed)
    ↓
Provider (TranslationProvider)
    ↓
业务逻辑 (translate方法)
    ↓
API服务 (ApiService)
    ↓
HTTP请求
    ↓
后端服务器
    ↓
JSON响应
    ↓
解析数据 (TranslationResult)
    ↓
更新状态 (notifyListeners)
    ↓
UI重建 (Consumer)
    ↓
显示结果
```

---

## ✅ 学习路径

### 初级（理解结构）
1. 阅读 [QUICKSTART.md](QUICKSTART.md)
2. 运行项目，看应用工作
3. 查看 [home_screen.dart](lib/screens/home_screen.dart) 理解UI

### 中级（修改功能）
1. 研究 [translation_provider.dart](lib/providers/translation_provider.dart)
2. 理解 [api_service.dart](lib/services/api_service.dart)
3. 尝试修改API地址或UI样式

### 高级（扩展功能）
1. 阅读 [DEVELOPMENT.md](DEVELOPMENT.md)
2. 添加新页面和功能
3. 优化性能，添加测试

---

## 🆘 快速解决方案

| 问题 | 解决方案 |
|------|---------|
| 应用无法启动 | `flutter clean && flutter pub get` |
| UI显示错乱 | 检查屏幕方向和尺寸 |
| API连接失败 | 检查后端运行，API地址 |
| 编译错误 | `flutter pub get` 和 `flutter clean` |
| iOS pod错误 | `cd ios && rm -rf Pods && pod install` |

---

## 📖 相关文档

- [Flutter官网](https://flutter.dev)
- [Dart文档](https://dart.dev)
- [Provider包](https://pub.dev/packages/provider)
- [Material Design 3](https://m3.material.io/)

---

**提示**: 按照文件名前面的⭐数量，优先学习和修改重要文件。
**⭐⭐⭐** = 必读必懂
**⭐⭐** = 重要，可能需要修改
**⭐** = 可选，了解即可

祝开发愉快！🚀
