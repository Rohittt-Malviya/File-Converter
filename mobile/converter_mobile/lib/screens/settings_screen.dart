import 'package:flutter/material.dart';
import 'package:permission_handler/permission_handler.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  Future<void> _requestStoragePermission(BuildContext context) async {
    final status = await Permission.storage.request();
    if (!context.mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(status.isGranted ? 'Storage access granted.' : 'Storage access was not granted.')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: ListView(
        children: [
          const ListTile(
            leading: Icon(Icons.shield_outlined),
            title: Text('Privacy first'),
            subtitle: Text('Files are processed locally and never uploaded.'),
          ),
          ListTile(
            leading: const Icon(Icons.folder_open),
            title: const Text('Request storage access'),
            onTap: () => _requestStoragePermission(context),
          ),
          const AboutListTile(
            applicationName: 'Local Convert',
            applicationVersion: '1.0.0',
            applicationLegalese: 'Local conversion without uploads.',
          ),
        ],
      ),
    );
  }
}
