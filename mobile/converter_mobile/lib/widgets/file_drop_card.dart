import 'package:flutter/material.dart';

class FileDropCard extends StatelessWidget {
  const FileDropCard({super.key, required this.onPressed});

  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onPressed,
      borderRadius: BorderRadius.circular(20),
      child: Ink(
        padding: const EdgeInsets.all(28),
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.surfaceContainerHighest,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: Theme.of(context).colorScheme.outlineVariant),
        ),
        child: const Column(
          children: [
            Icon(Icons.file_upload_outlined, size: 44),
            SizedBox(height: 12),
            Text('Choose files', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
            SizedBox(height: 6),
            Text('Text and image files are converted locally on your device.'),
          ],
        ),
      ),
    );
  }
}
