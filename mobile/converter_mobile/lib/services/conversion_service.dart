import 'dart:typed_data';

import '../models/conversion_file.dart';
import 'converter_service.dart';
import 'image_service.dart';
import 'pdf_service.dart';

class ConversionService {
  ConversionService({
    ConverterService? textAndImage,
    ImageService? images,
    PdfService? pdfs,
  })  : _textAndImage = textAndImage ?? ConverterService(),
        _images = images ?? ImageService(),
        _pdfs = pdfs ?? PdfService();

  final ConverterService _textAndImage;
  final ImageService _images;
  final PdfService _pdfs;

  List<String> supportedOutputs(List<ConversionFile> files) =>
      _textAndImage.supportedOutputs(files);

  Future<ConvertedFile> convert(ConversionFile file, String target) async {
    if (target == 'pdf' && ConverterService.textExtensions.contains(file.extension)) {
      final text = String.fromCharCodes(file.bytes);
      return ConvertedFile(
        name: '${file.name.replaceFirst(RegExp(r'\.[^.]+$'), '')}.pdf',
        bytes: await _pdfs.createTextPdf(text, title: file.name),
      );
    }
    if (ConverterService.imageExtensions.contains(file.extension) &&
        {'png', 'jpg', 'jpeg', 'webp'}.contains(target)) {
      return ConvertedFile(
        name: '${file.name.replaceFirst(RegExp(r'\.[^.]+$'), '')}.$target',
        bytes: _images.convert(Uint8List.fromList(file.bytes), target),
      );
    }
    return _textAndImage.convert(file, target);
  }
}
