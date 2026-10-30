import 'package:flutter/material.dart';

class FormatSelector extends StatelessWidget {
  const FormatSelector({
    super.key,
    required this.formats,
    required this.value,
    required this.onChanged,
  });

  final List<String> formats;
  final String? value;
  final ValueChanged<String?> onChanged;

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<String>(
      value: value,
      decoration: const InputDecoration(
        labelText: 'Convert to',
        border: OutlineInputBorder(),
      ),
      items: formats
          .map((format) => DropdownMenuItem(value: format, child: Text(format.toUpperCase())))
          .toList(),
      onChanged: onChanged,
    );
  }
}
