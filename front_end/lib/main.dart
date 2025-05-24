import 'dart:developer';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:pc_assistant/notifiers/theme_notifier.dart';
import 'package:pc_assistant/python_bridge/python_bridge.dart';
import 'package:pc_assistant/services/entry_point.dart';
import 'package:pc_assistant/theme/dark_theme.dart';
import 'package:pc_assistant/theme/light_theme.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

final themeNotifier = ThemeNotifier();

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  log('Starting Python Bridge');
  final pythonBridge = PythonBridge();
  await pythonBridge.start();
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
