import 'package:flutter/material.dart';

final ThemeData lightTheme = ThemeData(
  brightness: Brightness.light,
  scaffoldBackgroundColor: Colors.white,
  appBarTheme: const AppBarTheme(
    backgroundColor: Color(0xFF212121),
    foregroundColor: Colors.white,
    iconTheme: IconThemeData(color: Colors.black),
    titleTextStyle: TextStyle(
      color: Colors.white,
      fontSize: 20,
      fontWeight: FontWeight.bold,
    ),
  ),
  iconTheme: const IconThemeData(color: Colors.black, size: 28),
  floatingActionButtonTheme: const FloatingActionButtonThemeData(
    backgroundColor: Color(0xFFD6D6D6),
    foregroundColor: Colors.black,
    elevation: 0,
  ),
  iconButtonTheme: IconButtonThemeData(
    style: ButtonStyle(
      foregroundColor: WidgetStateProperty.all<Color>(Colors.black),
    ),
  ),
  textTheme: const TextTheme(
    bodyLarge: TextStyle(
      color: Colors.black,
      fontSize: 24,
      fontWeight: FontWeight.normal,
    ),
  ),
  cardColor: Color(0xFF5E5E5E),
  dividerColor: Color(0xFFD6D6D6),
);
