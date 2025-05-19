import 'package:shared_preferences/shared_preferences.dart';

class UserService {
  Future<String> loadUsername() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('username') ?? '';
  }

  Future<void> saveUsername(String name) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('username', name);
  }
}
