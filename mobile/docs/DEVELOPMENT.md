# Flutter项目配置参考

## 环境变量配置（可选）

如果需要根据不同环境使用不同的API地址，可以创建配置文件。

### 创建环境配置

在 `lib/config/app_config.dart` 中：

```dart
class AppConfig {
  static const String devApiBaseUrl = 'http://localhost:5001';
  static const String prodApiBaseUrl = 'https://api.example.com';
  
  static bool get isDev => const String.fromEnvironment('ENV') == 'dev';
  static String get apiBaseUrl => isDev ? devApiBaseUrl : prodApiBaseUrl;
}
```

然后在运行时指定环境：

```bash
flutter run --dart-define=ENV=prod
```

## 性能优化建议

### 1. 使用const构造函数

```dart
// ✅ 好的做法
const SizedBox(height: 20)

// ❌ 避免
SizedBox(height: 20)
```

### 2. 避免rebuild

使用 `const` 和 `final` 来防止不必要的重建：

```dart
// ✅ 推荐
class MyWidget extends StatelessWidget {
  const MyWidget({Key? key}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return const Text('Hello');
  }
}
```

### 3. Consumer细粒度控制

```dart
// ✅ 只在需要的地方使用Consumer
Column(
  children: [
    const SizedBox(height: 20),
    Consumer<TranslationProvider>(
      builder: (context, provider, _) {
        return Text(provider.result?.translation ?? '');
      },
    ),
  ],
)
```

## 国际化（i18n）

如需添加多语言支持，安装依赖：

```yaml
dependencies:
  intl: ^0.18.0
  # 或使用
  easy_localization: ^5.0.0
```

## 常用命令速查

```bash
# 清理构建缓存
flutter clean

# 升级依赖
flutter pub upgrade

# 获取依赖
flutter pub get

# 运行所有测试
flutter test

# 分析代码
flutter analyze

# 生成build
flutter gen-l10n

# 格式化代码
dart format .

# 静态分析
dart analyze
```

## VS Code快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+Shift+P` | 命令面板 |
| `Ctrl+F5` | 启动调试 |
| `Ctrl+Shift+F5` | 重启应用 |
| `r` | 热重载 |
| `R` | 完全重启 |
| `q` | 退出 |

## 单元测试示例

创建 `test/providers/translation_provider_test.dart`：

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:ai_translator/providers/translation_provider.dart';

void main() {
  group('TranslationProvider', () {
    test('初始状态检查', () {
      final provider = TranslationProvider();
      expect(provider.isLoading, false);
      expect(provider.result, null);
    });

    test('翻译调用', () async {
      final provider = TranslationProvider();
      await provider.translate('你好');
      expect(provider.isLoading, false);
    });
  });
}
```

运行测试：
```bash
flutter test
```

## 代码风格指南

### 变量命名

```dart
// ✅ 推荐
final userName = 'John';
const apiBaseUrl = 'http://...';
var result = [1, 2, 3];

// ❌ 避免
var userName = 'John';  // 应该用final
final API_BASE_URL = 'http://...';  // 应该用const
```

### 函数命名

```dart
// ✅ 推荐
void handleTranslate() {}
String? getTranslationResult() {}
bool isLoading() {}

// ❌ 避免
void Handle_Translate() {}  // 应该用camelCase
String getTranslationresult() {}
```

### 类命名

```dart
// ✅ 推荐
class TranslationProvider extends ChangeNotifier {}
class HomeScreen extends StatefulWidget {}

// ❌ 避免
class translation_provider extends ChangeNotifier {}  // 应该用PascalCase
class homescreen extends StatefulWidget {}
```

## 依赖管理

### 添加新依赖

```bash
# 添加依赖
flutter pub add package_name

# 添加dev依赖
flutter pub add --dev package_name

# 添加特定版本
flutter pub add package_name:^1.0.0
```

### 更新依赖

```bash
# 更新所有依赖到允许的最高版本
flutter pub upgrade

# 获取最新版本（可能有破坏性改动）
flutter pub upgrade --major-versions
```

## 调试技巧

### 打印日志

```dart
// 在Flutter中打印
debugPrint('Debug message');
print('Regular message');

// 使用日志库（推荐）
import 'dart:developer' as developer;
developer.log('Message', name: 'my.app');
```

### 断点调试

1. 在代码中点击行号旁边设置断点
2. 按 `Ctrl+F5` 启动调试
3. 使用调试工具栏：单步、继续、停止等

### 性能分析

```bash
# 运行应用并启用性能监控
flutter run --profile
```

然后打开DevTools检查帧率和性能指标。

## 常见错误解决

### "Cannot find plugin flutter_plugin_android_lifecycle"

```bash
flutter clean
flutter pub get
```

### iOS pod依赖冲突

```bash
cd ios
rm -rf Pods Pod.lock
pod repo update
pod install
cd ..
flutter run
```

### 编译错误"Gradle build failed"

```bash
cd android
./gradlew clean
cd ..
flutter clean
flutter pub get
flutter run
```

## 发布前检查

1. **版本号**: 
   - `pubspec.yaml` 中的 `version`
   - Android: `android/app/build.gradle` 中的 `versionCode` 和 `versionName`
   - iOS: Xcode中的Build版本

2. **签名**:
   - Android: 需要配置 `keystore` 和签名密钥
   - iOS: 需要Apple Developer证书

3. **测试**:
   ```bash
   flutter test
   flutter integration_test
   ```

4. **性能**:
   ```bash
   flutter run --release
   # 检查应用大小和加载时间
   ```

## 相关资源

- [Flutter官网](https://flutter.dev)
- [Pub.dev包库](https://pub.dev)
- [Flutter社区](https://flutter.dev/community)
- [Stack Overflow - Flutter标签](https://stackoverflow.com/questions/tagged/flutter)
