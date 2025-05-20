import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:shared_preferences/shared_preferences.dart';

Future<String?> saveNickname(
  TextEditingController controller,
  BuildContext context,
) async {
  final nickname = controller.text.trim();
  if (nickname.isEmpty) return null;

  final prefs = await SharedPreferences.getInstance();
  await prefs.setString('nickname', nickname);
  return nickname;
}
