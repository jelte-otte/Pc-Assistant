import 'package:flutter/material.dart';

final ThemeData darkTheme = ThemeData(
  brightness: Brightness.dark,
  scaffoldBackgroundColor: Color(0xFF121212),
  appBarTheme: const AppBarTheme(
    backgroundColor: Color(0xFF1E1E1E),
    foregroundColor: Colors.white,
    iconTheme: IconThemeData(color: Colors.white),
    titleTextStyle: TextStyle(
      color: Colors.white,
      fontSize: 20,
      fontWeight: FontWeight.bold,
    ),
  ),
  iconTheme: const IconThemeData(
    color: Colors.white,
    size: 28,
  ),
  floatingActionButtonTheme: const FloatingActionButtonThemeData(
    backgroundColor: Color(0xFF2E2E2E),
    foregroundColor: Colors.white,
    elevation: 0,
  ),
  textTheme: const TextTheme(
    bodyLarge: TextStyle(
      color: Colors.white,
      fontSize: 24,
      fontWeight: FontWeight.normal,
    ),
    bodyMedium: TextStyle(
      color: Color(0xFFBDBDBD),
    ),
  ),
  cardColor: Color(0xFF5E5E5E),
  dividerColor: Color(0xFF2E2E2E),
);
