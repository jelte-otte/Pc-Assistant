import 'package:flutter/material.dart';
import 'package:frontend/widgets/base_dialog.dart';
import 'package:frontend/widgets/nickname_input.dart';

class Settings extends StatefulWidget {
  const Settings({super.key});

  @override
  State<Settings> createState() => _SettingsState();
}

class _SettingsState extends State<Settings> {
  bool isDarkMode = false;

  @override
  Widget build(BuildContext context) {
    return BaseDialog(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text(
            'Settings',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 20),
          ListTile(
            title: const Text('Toggle Theme'),
            trailing: GestureDetector(
              onTap: () {
                setState(() {
                  isDarkMode = !isDarkMode;
                });
              },
              child: AnimatedContainer(
                duration: Duration(milliseconds: 200),
                width: 80,
                height: 40,
                padding: EdgeInsets.all(5),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(20),
                  color: isDarkMode ? Colors.grey[800] : Colors.yellow[600],
                ),
                child: AnimatedAlign(
                  duration: Duration(milliseconds: 300),
                  curve: Curves.easeInOut,
                  alignment:
                      isDarkMode ? Alignment.centerRight : Alignment.centerLeft,
                  child: AnimatedSwitcher(
                    duration: Duration(milliseconds: 300),
                    transitionBuilder:
                        (child, animation) =>
                            FadeTransition(opacity: animation, child: child),
                    child: Icon(
                      isDarkMode ? Icons.nightlight_round : Icons.wb_sunny,
                      key: ValueKey<bool>(isDarkMode),
                      color: isDarkMode ? Colors.white : Colors.orange,
                      size: 24,
                    ),
                  ),
                ),
              ),
            ),
          ),
          const Divider(),
          ListTile(
            title: const Text('Change Nickname'),
            onTap: () {
              Navigator.of(context).pop(); // sluit huidige dialog
              showDialog(
                context: context,
                builder: (context) => const UsernameInput(),
              );
            },
          ),
        ],
      ),
    );
  }
}
