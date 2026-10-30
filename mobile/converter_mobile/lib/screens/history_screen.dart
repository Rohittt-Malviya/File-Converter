import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final date = DateFormat.yMMMd().add_jm().format(DateTime.now());
    return Scaffold(
      appBar: AppBar(title: const Text('History')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          const Icon(Icons.history, size: 56),
          const SizedBox(height: 12),
          const Center(child: Text('Recent conversions will appear here.')),
          const SizedBox(height: 24),
          Card(
            child: ListTile(
              leading: const Icon(Icons.info_outline),
              title: const Text('Conversion history is local'),
              subtitle: Text('Last checked $date'),
            ),
          ),
        ],
      ),
    );
  }
}
