import 'package:flutter/material.dart';
import 'package:frontend/widgets/base_dialog.dart';

class UsernameInput extends StatefulWidget {
  const UsernameInput({super.key});

  @override
  State<UsernameInput> createState() => _UsernameInputState();
}

class _UsernameInputState extends State<UsernameInput> {
  String nickname = "default_nickname";

  @override
  Widget build(BuildContext context) {
    return BaseDialog(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          SizedBox(height: 10),
          const Text(
            'Enter your nickname',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 20),
          Text(
            "Your current nickname is: $nickname",
            style: TextStyle(
              fontSize: 16,
              fontStyle: FontStyle.italic,
              color: Colors.grey,
            ),
          ),
          const SizedBox(height: 75),
          SizedBox(
            width: 400,
            child: TextField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Nickname',
              ),
            ),
          ),
          const SizedBox(height: 30),
          SizedBox(
            width: 100,
            height: 50,
            child: ElevatedButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text(
                'Submit',
                style: TextStyle(color: Colors.black),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
