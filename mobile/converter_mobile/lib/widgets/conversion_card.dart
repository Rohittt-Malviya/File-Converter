import 'package:flutter/material.dart';

import '../models/conversion_file.dart';

class ConversionCard extends StatelessWidget {
  const ConversionCard({super.key, required this.file, this.onRemove});

  final ConversionFile file;
  final VoidCallback? onRemove;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: const Icon(Icons.insert_drive_file_outlined),
        title: Text(file.name),
        subtitle: Text('${file.size} bytes'),
        trailing: onRemove == null ? null : IconButton(icon: const Icon(Icons.close), onPressed: onRemove),
      ),
    );
  }
}
