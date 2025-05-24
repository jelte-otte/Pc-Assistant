import 'dart:convert';
import 'dart:developer';
import 'dart:io';

import 'package:flutter_dotenv/flutter_dotenv.dart';

class PythonBridge {
  Process? _process;
  IOSink? _stdin;
  late Stream<String> _stdoutStream;

  Future<void> start() async {
    _process = await Process.start(
      'python',
      ['check_for_dangerous_apps.py'],
      workingDirectory: dotenv.env['WORKING_DIRECTORY'] ?? '',
      runInShell: true,
    );
    _stdin = _process!.stdin;

    _stdoutStream = _process!.stdout
        .transform(utf8.decoder)
        .transform(const LineSplitter());

    _stdoutStream.listen((line) {
      log("Backend zei: $line");
    });
    _process!.stderr
        .transform(utf8.decoder)
        .transform(const LineSplitter())
        .listen((line) {
          log("Python stderr: $line");
        });

    _process!.exitCode.then((code) {
      log('Python script exited with code $code');
    });
  }

  void send(String text) {
    _stdin?.writeln(text);
  }

  void stop() {
    _process?.kill();
  }
}
