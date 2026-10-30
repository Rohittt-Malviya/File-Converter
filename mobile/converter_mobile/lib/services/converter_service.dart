import 'dart:convert';
import 'dart:typed_data';

import 'package:image/image.dart' as img;
import 'package:path/path.dart' as p;

import '../models/conversion_file.dart';

class ConvertedFile {
  const ConvertedFile({required this.name, required this.bytes});

  final String name;
  final Uint8List bytes;
}

class ConverterService {
  static const textExtensions = {'txt', 'md', 'csv', 'json'};
  static const imageExtensions = {'png', 'jpg', 'jpeg', 'webp'};

  List<String> supportedOutputs(List<ConversionFile> files) {
    if (files.isEmpty) return const [];
    final extensions = files.map((file) => file.extension).toSet();
    if (extensions.every(textExtensions.contains)) {
      return textExtensions.difference(extensions).toList()..sort();
    }
    if (extensions.every(imageExtensions.contains)) {
      return ['png', 'jpg', 'webp'].where((item) => !extensions.contains(item)).toList();
    }
    return const [];
  }

  Future<ConvertedFile> convert(
    ConversionFile file,
    String targetExtension,
  ) async {
    if (textExtensions.contains(file.extension) &&
        textExtensions.contains(targetExtension)) {
      return _convertText(file, targetExtension);
    }
    if (imageExtensions.contains(file.extension) &&
        imageExtensions.contains(targetExtension)) {
      return _convertImage(file, targetExtension);
    }
    throw UnsupportedError(
      'Conversion from ${file.extension.isEmpty ? 'unknown' : file.extension} '
      'to $targetExtension is not supported.',
    );
  }

  ConvertedFile _convertText(ConversionFile file, String target) {
    final text = utf8.decode(file.bytes, allowMalformed: true);
    var output = text;
    if (target == 'json' && file.extension != 'json') {
      if (file.extension == 'csv') {
        final rows = const LineSplitter()
            .convert(text)
            .where((row) => row.trim().isNotEmpty)
            .map((row) => row.split(',').map((cell) => cell.trim()).toList())
            .toList();
        if (rows.isEmpty) {
          output = '[]';
        } else {
          final headers = rows.first;
          output = const JsonEncoder.withIndent('  ').convert(
            rows.skip(1).map((row) {
              return <String, String>{
                for (var i = 0; i < headers.length; i++)
                  headers[i]: i < row.length ? row[i] : '',
              };
            }).toList(),
          );
        }
      } else {
        output = const JsonEncoder.withIndent('  ').convert({'content': text});
      }
    }
    final name = '${p.basenameWithoutExtension(file.name)}.$target';
    return ConvertedFile(name: name, bytes: Uint8List.fromList(utf8.encode(output)));
  }

  ConvertedFile _convertImage(ConversionFile file, String target) {
    final decoded = img.decodeImage(file.bytes);
    if (decoded == null) throw const FormatException('The image could not be decoded.');
    final encoded = switch (target) {
      'png' => img.encodePng(decoded),
      'jpg' => img.encodeJpg(decoded),
      'webp' => img.encodeWebP(decoded),
      _ => throw UnsupportedError('Unsupported image output: $target'),
    };
    return ConvertedFile(
      name: '${p.basenameWithoutExtension(file.name)}.$target',
      bytes: Uint8List.fromList(encoded),
    );
  }
}
