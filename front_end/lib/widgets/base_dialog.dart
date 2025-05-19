import 'package:flutter/material.dart';

class BaseDialog extends StatelessWidget {
  final Widget child;

  const BaseDialog({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
      child: SizedBox(
        width: 500,
        height: 400,
        child: child,
      ),
    );
  }
}
