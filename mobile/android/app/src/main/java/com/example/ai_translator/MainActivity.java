package com.example.ai_translator;

import android.os.Build;
import android.os.Bundle;
import androidx.core.splashscreen.SplashScreen;
import io.flutter.embedding.android.FlutterActivity;

public class MainActivity extends FlutterActivity {
  @Override
  protected void onCreate(Bundle savedInstanceState) {
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
      SplashScreen.installSplashScreen(this);
    }
    super.onCreate(savedInstanceState);
  }
}
