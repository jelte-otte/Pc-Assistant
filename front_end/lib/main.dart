import 'package:flutter/material.dart';
import 'package:frontend/theme/light_theme.dart';
import 'package:frontend/theme/dark_theme.dart';
import 'package:frontend/views/home_page.dart';
import 'package:frontend/notifiers/theme_notifier.dart';

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
      home: const HomePage(),
    );
  }
}
