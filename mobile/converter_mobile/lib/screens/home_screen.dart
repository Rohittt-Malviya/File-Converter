import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

import '../models/conversion_file.dart';
import '../services/conversion_service.dart';
import '../services/file_service.dart';
import '../widgets/conversion_card.dart';
import '../widgets/file_drop_card.dart';
import '../widgets/format_selector.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _converter = ConversionService();
  final _fileService = FileService();
  final _files = <ConversionFile>[];
  String? _target;
  String? _status;
  bool _busy = false;

  Future<void> _pickFiles() async {
    final result = await FilePicker.platform.pickFiles(
      allowMultiple: true,
      withData: true,
    );
    if (result == null) return;
    final picked = result.files
        .where((file) => file.bytes != null)
        .map((file) => ConversionFile(name: file.name, bytes: file.bytes!))
        .toList();
    setState(() {
      _files
        ..clear()
        ..addAll(picked);
      _target = null;
      _status = picked.isEmpty ? 'The selected files could not be read.' : null;
    });
  }

  Future<void> _convert() async {
    if (_target == null || _files.isEmpty) return;
    setState(() {
      _busy = true;
      _status = 'Converting locally…';
    });
    try {
      for (final file in _files) {
        final converted = await _converter.convert(file, _target!);
        await _fileService.saveAndShare(converted);
      }
      setState(() => _status = 'Converted ${_files.length} file${_files.length == 1 ? '' : 's'}.');
    } catch (error) {
      setState(() => _status = error.toString().replaceFirst('Exception: ', ''));
    } finally {
      setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final outputs = _converter.supportedOutputs(_files);
    return Scaffold(
      appBar: AppBar(title: const Text('Local Convert')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Text('Private file conversion', style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 8),
          const Text('No uploads, accounts, or analytics. Your files stay on this device.'),
          const SizedBox(height: 24),
          FileDropCard(onPressed: _pickFiles),
          if (_files.isNotEmpty) ...[
            const SizedBox(height: 24),
            Row(
              children: [
                Text('Selected files (${_files.length})', style: Theme.of(context).textTheme.titleMedium),
                const Spacer(),
                TextButton(onPressed: _busy ? null : () => setState(_files.clear), child: const Text('Clear')),
              ],
            ),
            ..._files.map((file) => ConversionCard(
                  file: file,
                  onRemove: _busy
                      ? null
                      : () => setState(() => _files.remove(file)),
                )),
            if (outputs.isEmpty)
              const Text('Select files from one compatible format family.')
            else ...[
              const SizedBox(height: 12),
              FormatSelector(
                formats: outputs,
                value: _target,
                onChanged: _busy ? (_) {} : (value) => setState(() => _target = value),
              ),
              const SizedBox(height: 16),
              FilledButton.icon(
                onPressed: _busy || _target == null ? null : _convert,
                icon: const Icon(Icons.transform),
                label: Text(_busy ? 'Converting…' : 'Convert and share'),
              ),
            ],
          ],
          if (_status != null) ...[
            const SizedBox(height: 16),
            Text(_status!, textAlign: TextAlign.center),
          ],
        ],
      ),
    );
  }
}
