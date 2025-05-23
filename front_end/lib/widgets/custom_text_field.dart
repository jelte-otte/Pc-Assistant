import 'dart:async';
import 'dart:developer';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class NativeInputField extends StatefulWidget {
  final Function? function;
  final TextStyle? textStyle;
  final InputDecoration? inputDecoration;
  final Color? cursorColor;
  final TextInputType keyboardType;
  final Color? focusColor;
  final Color? allSelectedColor;
  final TextEditingController controller;

  const NativeInputField({
    super.key,
    this.function,
    this.textStyle,
    this.inputDecoration,
    this.cursorColor = Colors.black,
    this.keyboardType = TextInputType.text,
    this.focusColor,
    this.allSelectedColor,
    required this.controller,
  });

  @override
  State<NativeInputField> createState() => _NativeInputFieldState();
}

class _NativeInputFieldState extends State<NativeInputField>
    with SingleTickerProviderStateMixin {
  String _text = '';
  final MethodChannel _inputChannel = const MethodChannel('input.channel');
  final MethodChannel _focusChannel = const MethodChannel('focus.channel');
  final FocusNode _focusNode = FocusNode();
  bool _showCursor = true;
  int _cursorPosition = 0;
  Timer? _cursorTimer;
  bool _isAllSelected = false;
  bool _isTyping = false; // Nieuwe variabele om type-status bij te houden
  Timer? _typingTimer; // Timer om te detecteren wanneer typen stopt
  final Color fallbackAllSelectedColor = Colors.blue.withAlpha(
    (0.3 * 255).toInt(),
  );
  final Color fallbackFocusColor = Colors.blue.withAlpha((0.3 * 255).toInt());

  late TextEditingController _controller;

  @override
  void initState() {
    super.initState();
    _controller = widget.controller;

    _inputChannel.setMethodCallHandler((call) async {
      log('Received from native: ${call.method}, ${call.arguments}');
      if (call.method == 'input') {
        setState(() {
          // Start typing timer om te detecteren wanneer typen stopt
          _isTyping = true;
          _showCursor = true; // Cursor constant tonen tijdens typen
          _typingTimer?.cancel();
          _typingTimer = Timer(const Duration(milliseconds: 500), () {
            setState(() {
              _isTyping = false; // Typen gestopt, cursor kan weer knipperen
            });
          });

          if (call.arguments == 'BACKSPACE') {
            if (_text.isNotEmpty) {
              if (_isAllSelected) {
                _text = '';
                _cursorPosition = 0;
                _isAllSelected = false;
              } else if (_text.isNotEmpty) {
                _text = _text.substring(0, _text.length - 1);
                _cursorPosition = _text.length.clamp(0, _text.length);
              }
            }
          } else if (call.arguments == 'CTRL_BACKSPACE') {
            final words = _text.trim().split(RegExp(r'\s+'));
            if (words.isNotEmpty) {
              words.removeLast();
              _text = words.join(' ') + (words.isNotEmpty ? ' ' : '');
              _cursorPosition = _text.length.clamp(0, _text.length);
            }
            _isAllSelected = false;
          } else if (call.arguments == 'ENTER') {
            widget.function?.call();
            _isAllSelected = false;
          } else if (call.arguments == 'SHIFT_ENTER') {
            _text += '\n';
            _cursorPosition = _text.length;
            _isAllSelected = false;
          } else if (call.arguments == 'SELECT_ALL') {
            _isAllSelected = true;
          } else {
            _text += call.arguments as String;
            _cursorPosition = _text.length;
            _isAllSelected = false;
          }
        });

        _controller.text = _text;
      } else if (call.method == 'focus') {
        if (call.arguments == true) {
          _focusNode.requestFocus();
          setState(() {});
        }
      }
      return null;
    });
  }

  @override
  void dispose() {
    _cursorTimer?.cancel();
    _typingTimer?.cancel(); // Vergeet typing timer niet
    _focusNode.dispose();
    super.dispose();
  }

  Future<void> _requestNativeFocus() async {
    try {
      await _focusChannel.invokeMethod('focus');
    } catch (e) {
      log('Fout bij het aanvragen van focus: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_focusNode.hasFocus && _cursorTimer == null && !_isTyping) {
      _cursorTimer = Timer.periodic(const Duration(milliseconds: 750), (timer) {
        setState(() {
          _showCursor = !_showCursor;
        });
      });
    } else if (!_focusNode.hasFocus || _isTyping) {
      _cursorTimer?.cancel();
      _cursorTimer = null;
      if (!_focusNode.hasFocus) {
        _showCursor = false;
        _isAllSelected = false;
      } else {
        _showCursor = true; // Cursor constant tonen tijdens typen
      }
      setState(() {});
    }

    final textStyle =
        widget.textStyle ??
        TextStyle(
          fontSize: 16,
          color: _text.isEmpty ? Colors.grey : Colors.black,
          backgroundColor:
              _isAllSelected
                  ? (widget.allSelectedColor ?? fallbackAllSelectedColor)
                  : null,
        );

    return Focus(
      focusNode: _focusNode,
      onFocusChange: (hasFocus) {
        log('Focus changed: $hasFocus');
        if (hasFocus) {
          _requestNativeFocus();
        } else {
          _cursorTimer?.cancel();
          _cursorTimer = null;
          _typingTimer?.cancel();
          _typingTimer = null;
          _showCursor = false;
          _isAllSelected = false;
        }
        setState(() {});
      },
      child: GestureDetector(
        onTap: () {
          log('Tapped on field');
          _focusNode.requestFocus();
          _requestNativeFocus();
          setState(() {});
        },
        child: InputDecorator(
          decoration:
              widget.inputDecoration ??
              InputDecoration(
                border: const OutlineInputBorder(),
                isDense: true,
                filled: _focusNode.hasFocus,
                fillColor:
                    _focusNode.hasFocus
                        ? (widget.focusColor ?? fallbackFocusColor)
                        : Colors.transparent,
              ),
          isFocused: _focusNode.hasFocus,
          isEmpty: _text.isEmpty,
          child: LayoutBuilder(
            builder: (context, constraints) {
              return SizedBox(
                width: constraints.maxWidth,
                child: RichText(
                  text: TextSpan(
                    children: [
                      TextSpan(text: _text, style: textStyle),
                      if (_focusNode.hasFocus && _showCursor && !_isAllSelected)
                        WidgetSpan(
                          child: Container(
                            width: 2,
                            height: 16,
                            color: widget.cursorColor,
                            margin: EdgeInsets.only(
                              left: _cursorPosition > 0 ? 2.0 : 0.0,
                            ),
                          ),
                        ),
                    ],
                  ),
                  maxLines: null,
                  textAlign: TextAlign.left,
                ),
              );
            },
          ),
        ),
      ),
    );
  }
}
