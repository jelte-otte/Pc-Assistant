import 'package:flutter/material.dart';
import 'package:pc_assistant/notifiers/theme_notifier.dart';
import 'package:pc_assistant/services/entry_point.dart';
import 'package:pc_assistant/test.dart';
import 'package:pc_assistant/theme/dark_theme.dart';
import 'package:pc_assistant/theme/light_theme.dart';

final themeNotifier = ThemeNotifier();

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Flutter Demo',
      theme: lightTheme,
      darkTheme: darkTheme,
      themeMode: ThemeMode.light,
      home: EntryPoint(),
    );
  }
}
