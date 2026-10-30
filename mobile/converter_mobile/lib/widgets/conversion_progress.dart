import 'package:flutter/material.dart';

class ConversionProgress extends StatelessWidget {
  const ConversionProgress({super.key, required this.progress, this.label});

  final double progress;
  final String? label;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        if (label != null) Text(label!),
        const SizedBox(height: 8),
        LinearProgressIndicator(value: progress.clamp(0, 1)),
      ],
    );
  }
}
