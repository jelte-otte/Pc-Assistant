import 'package:flutter/material.dart';
import 'package:pc_assistant/utils/load_nickname.dart';
import 'package:pc_assistant/widgets/drawer.dart';
import 'package:pc_assistant/widgets/nickname_input.dart';
import 'package:pc_assistant/widgets/settings.dart';
import 'dart:convert';
import 'dart:io';

class HomePage extends StatefulWidget {
  final bool openNicknameInput;
  const HomePage({super.key, this.openNicknameInput = false});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String nickname = '';
  bool isPressed = false;
  final _controller = TextEditingController();
  final pythonBridge = PythonBridge(); 
  @override
  void initState() {
    print('Werkdirectory: ${Directory.current.path}');
    super.initState();
    pythonBridge.start().then((_) {
    print("Sending test input...");
    pythonBridge.send("hallo");
  });
    loadNickname().then((storedNickname) {
      setState(() {
        nickname = storedNickname;
      });
    });
    if (widget.openNicknameInput) {
      Future.microtask(() async {
        final newNickname = await showDialog<String>(
          context: context,
          builder: (context) => const NicknameInput(),
          barrierDismissible: false,
        );
        if (newNickname != null && mounted) {
          setState(() {
            nickname = newNickname;
          });
        }
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: AppDrawer(),
      body: SafeArea(
        child: Stack(
          children: [
            Positioned(
              top: 8,
              left: 8,
              child: Builder(
                builder: (context) {
                  return IconButton(
                    icon: const Icon(Icons.menu),
                    onPressed: () {
                      Scaffold.of(context).openDrawer();
                    },
                    iconSize: 40,
                  );
                },
              ),
            ),
            Positioned(
              top: 8,
              right: 8,
              child: IconButton(
                icon: const Icon(Icons.settings),
                onPressed: () async {
                  final updatedNickname = await showDialog<String>(
                    context: context,
                    builder: (context) => const Settings(),
                  );
                  if (updatedNickname != null && mounted) {
                    setState(() {
                      nickname = updatedNickname;
                    });
                  }
                },
                iconSize: 40,
              ),
            ),
            Positioned(
              top: 100,
              left: 0,
              right: 0,
              child: Center(
                child: Text(
                  '👋 Good to see you $nickname',
                  style: TextStyle(fontSize: 30),
                ),
              ),
            ),
            Positioned(
              left: 0,
              right: 0,
              top: 250,
              child: Center(
                child: GestureDetector(
                  child: Container(
                    width: 250,
                    height: 250,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: Color(0xFF5E5E5E),
                      boxShadow: [
                        BoxShadow(
                          color:
                              isPressed
                                  ? Colors.transparent
                                  : Color.fromARGB(146, 158, 158, 158),
                          blurRadius: 7,
                          spreadRadius: 5,
                          offset: Offset(0, 3),
                        ),
                      ],
                    ),
                  ),
                  onTapDown: (TapDownDetails details) {
                    setState(() {
                      isPressed = true;
                    });
                  },
                  onTapUp: (TapUpDetails details) {
                    setState(() {
                      isPressed = false;
                    });
                  },
                ),
              ),
            ),
            Positioned(
              bottom: 150,
              left: 0,
              right: 0,
              child: Center(
                child: Row(
                  children: [
                    SizedBox(
                      width: 500,
                      child: TextField(
                        controller: _controller,
                        decoration: InputDecoration(
                          hintText: 'ask me anything...',
                          hintStyle: TextStyle(
                            color: Color(0xFF5E5E5E),
                            fontSize: 20,
                          ),
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(20),
                            borderSide: BorderSide(
                              color: Color(0xFF5E5E5E),
                              width: 2,
                            ),
                          ),
                          focusedBorder: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(20),
                            borderSide: BorderSide(
                              color: Color(0xFF5E5E5E),
                              width: 2.3,
                            ),
                          ),
                        ),
                      ),
                    ),
                    IconButton(onPressed: (){pythonBridge.send(_controller.text);}, icon: Icon(Icons.send))
                  ],
                ),
              ),
            ), // ),
          ],
        ),
      ),
    );
  }
}

class PythonBridge {
  Process? _process;
  IOSink? _stdin;
  late Stream<String> _stdoutStream;

  Future<void> start() async {
    _process = await Process.start(
      'python3',
      ['../call_assistant.py'],
      runInShell: true,
    );
    _stdin = _process!.stdin;

    _stdoutStream = _process!.stdout
        .transform(utf8.decoder)
        .transform(const LineSplitter());

    _stdoutStream.listen((line) {
      print("Backend zei: $line");
    });
  }

  void send(String text) {
    _stdin?.writeln(text);
  }

  void stop() {
    _process?.kill();
  }
}
