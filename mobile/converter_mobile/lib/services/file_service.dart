import 'dart:io';

import 'package:path_provider/path_provider.dart';
import 'package:share_plus/share_plus.dart';

import 'converter_service.dart';

class FileService {
  Future<void> saveAndShare(ConvertedFile file) async {
    final directory = await getTemporaryDirectory();
    final output = File('${directory.path}/${file.name}');
    await output.writeAsBytes(file.bytes, flush: true);
    await Share.shareXFiles([XFile(output.path)], text: file.name);
  }
}
