import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class CustomInputField extends StatefulWidget {
  const CustomInputField({super.key});

  @override
  State<CustomInputField> createState() => _CustomInputFieldState();
}

class _CustomInputFieldState extends State<CustomInputField> {
  String _text = '';
  final FocusNode _focusNode = FocusNode();

  KeyEventResult _handleKeyEvent(FocusNode node, KeyEvent event) {
    if (event is KeyDownEvent) {
      final key = event.logicalKey;

      setState(() {
        if (key == LogicalKeyboardKey.backspace && _text.isNotEmpty) {
          _text = _text.substring(0, _text.length - 1);
        } else if (key == LogicalKeyboardKey.enter) {
          // Verwerk de invoer
          print("Invoer bevestigd: $_text");
        } else if (key.keyLabel.length == 1) {
          _text += key.keyLabel;
        }
      });
    }

    return KeyEventResult.handled;
  }

  @override
  Widget build(BuildContext context) {
    return Focus(
      focusNode: _focusNode,
      onKeyEvent: _handleKeyEvent,
      child: GestureDetector(
        onTap: () => _focusNode.requestFocus(),
        child: Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            border: Border.all(color: Colors.grey),
            borderRadius: BorderRadius.circular(4),
          ),
          child: Text(
            _text.isEmpty ? 'Typ iets...' : _text,
            style: const TextStyle(fontSize: 18),
          ),
        ),
      ),
    );
  }
}
