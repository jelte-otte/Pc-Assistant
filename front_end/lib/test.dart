import 'package:flutter/material.dart';
import 'package:pc_assistant/widgets/custom_text_field.dart';

class Test extends StatefulWidget {
  const Test({super.key});

  @override
  State<Test> createState() => _TestState();
}

class _TestState extends State<Test> {
  final _controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(body: Center(child: NativeInputField(controller: _controller,)));
  }
}
