import 'package:flutter/material.dart';
import 'package:pc_assistant/utils/load_nickname.dart';
import 'package:pc_assistant/utils/save_nickname.dart';
import 'package:pc_assistant/widgets/base_dialog.dart';
import 'package:pc_assistant/widgets/custom_text_field.dart';

class NicknameInput extends StatefulWidget {
  const NicknameInput({super.key});

  @override
  State<NicknameInput> createState() => _NicknameInputState();
}

class _NicknameInputState extends State<NicknameInput> {
  final _controller = TextEditingController();
  final _focusNode = FocusNode();
  String nickname = '';
  String nicknameMessage = '';

  @override
  void initState() {
    super.initState();
    loadNickname().then((storedNickname) {
      if (mounted) {
        setState(() {
          nickname = storedNickname;
        });
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    _focusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    nicknameMessage =
        nickname.isEmpty
            ? 'Please enter a nickname to continue.'
            : 'Your current nickname is: $nickname';
    return BaseDialog(
      child: GestureDetector(
        onTap: () {
          if (mounted) {
            Navigator.pop(context);
          }
        },
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
              nicknameMessage,
              style: TextStyle(
                fontSize: 16,
                fontStyle: FontStyle.italic,
                color: Colors.grey,
              ),
            ),
            const SizedBox(height: 75),
            SizedBox(
              width: 400,
              child: NativeInputField(
                focusColor: Colors.transparent,
                inputDecoration: InputDecoration(
                  labelText: 'Nickname',
                  labelStyle: const TextStyle(
                    color: Colors.black,
                    fontSize: 20,
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderSide: BorderSide(color: Colors.black),
                  ),
                ),
                controller: _controller,
              ),
            ),
            const SizedBox(height: 30),
            SizedBox(
              width: 100,
              height: 50,
              child: ElevatedButton(
                onPressed: () async {
                  if (mounted) {
                    final newNickname = await saveNickname(
                      _controller,
                      context,
                    );
                    if (newNickname != null && context.mounted) {
                      Navigator.pop(context, newNickname);
                    }
                  }
                },
                child: const Text(
                  'Submit',
                  style: TextStyle(color: Colors.black),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
