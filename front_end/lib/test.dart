import 'package:flutter/material.dart';

class Test extends StatelessWidget {
  const Test({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          children: [
            TextField(
              decoration: InputDecoration(
                labelText: 'Testing',
                border: OutlineInputBorder(),
              ),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => Test1()),
                );
              },
              child: Text("PRESS HERE"),
            ),
          ],
        ),
      ),
    );
  }
}

class Test1 extends StatelessWidget {
  const Test1({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: const TextField(
          decoration: InputDecoration(
            labelText: 'Testing',
            border: OutlineInputBorder(),
          ),
        ),
      ),
    );
  }
}
