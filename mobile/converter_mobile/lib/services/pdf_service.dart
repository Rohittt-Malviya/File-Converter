import 'dart:typed_data';

import 'package:pdf/widgets.dart' as pw;

class PdfService {
  Future<Uint8List> createTextPdf(String text, {String title = 'Converted document'}) async {
    final document = pw.Document();
    document.addPage(
      pw.MultiPage(
        build: (_) => [
          pw.Header(level: 0, text: title),
          pw.Text(text),
        ],
      ),
    );
    return document.save();
  }
}
