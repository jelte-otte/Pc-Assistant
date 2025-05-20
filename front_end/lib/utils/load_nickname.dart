import 'package:shared_preferences/shared_preferences.dart';

Future<String> loadNickname() async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getString('nickname') ?? '';
}
