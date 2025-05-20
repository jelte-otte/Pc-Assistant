import 'package:flutter/material.dart';
import 'package:pc_assistant/views/home_page.dart';
import 'package:shared_preferences/shared_preferences.dart';

class EntryPoint extends StatefulWidget {
  const EntryPoint({super.key});

  @override
  EntryPointState createState() => EntryPointState();
}

class EntryPointState extends State<EntryPoint> {
  Future<bool> _hasNickname() async {
    final prefs = await SharedPreferences.getInstance();
    final nickname = prefs.getString('nickname');
    return nickname != null && nickname.isNotEmpty;
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<bool>(
      future: _hasNickname(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Scaffold(body: Center(child: CircularProgressIndicator()));
        }

        if (snapshot.hasData && snapshot.data!) {
          return HomePage();
        } else {
          return HomePage(openNicknameInput: true);
        }
      },
    );
  }
}