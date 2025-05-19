import 'package:flutter/material.dart';
import 'package:frontend/widgets/drawer.dart';
import 'package:frontend/widgets/settings.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String username = 'Jelte';
  bool isPressed = false;
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      drawer: AppDrawer(),
      body: SafeArea(
        child: Stack(
          children: [
            // Linker icoon (menu)
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

            // Rechter icoon (instellingen)
            Positioned(
              top: 8,
              right: 8,
              child: IconButton(
                icon: const Icon(Icons.settings),
                onPressed: () {
                  showDialog(
                    context: context,
                    builder: (context) => SizedBox(child: Settings()),
                  );
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
                  'Good to see you $username👋',
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
                          offset: Offset(0, 3), // changes position of shadow
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
                child: SizedBox(
                  width: 500,
                  child: TextField(
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
                          width: 2, // Realistische waarde
                        ),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(20),
                        borderSide: BorderSide(
                          color: Color(0xFF5E5E5E),
                          width: 2.3, // Realistische waarde
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ), // ),
          ],
        ),
      ),
    );
  }
}
