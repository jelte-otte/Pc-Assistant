import 'package:flutter/material.dart';

class AppDrawer extends StatelessWidget {
  const AppDrawer({super.key});

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        children: [
          SizedBox(
            height: 75,
            child: const DrawerHeader(
              decoration: BoxDecoration(color: Color(0xFF616161)),
              child: Text('Menu'),
            ),
          ),
          ListTile(title: Text("tile1"), onTap: () {}),
          ListTile(title: Text("tile2"), onTap: () {}),
          ListTile(title: Text("tile3"), onTap: () {}),
        ],
      ),
    );
  }
}
