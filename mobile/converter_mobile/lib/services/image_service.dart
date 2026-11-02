import 'dart:typed_data';

import 'package:image/image.dart' as img;
import 'package:image_picker/image_picker.dart';

class ImageService {
  final ImagePicker _picker = ImagePicker();

  Future<Uint8List?> pickFromGallery() async {
    final file = await _picker.pickImage(source: ImageSource.gallery);
    return file == null ? null : Uint8List.fromList(await file.readAsBytes());
  }

  Uint8List convert(Uint8List bytes, String targetExtension) {
    final decoded = img.decodeImage(bytes);
    if (decoded == null) throw const FormatException('The image could not be decoded.');
    final encoded = switch (targetExtension.toLowerCase()) {
      'png' => img.encodePng(decoded),
      'jpg' || 'jpeg' => img.encodeJpg(decoded),
      'webp' => img.encodeWebP(decoded),
      _ => throw UnsupportedError('Unsupported image output: $targetExtension'),
    };
    return Uint8List.fromList(encoded);
  }
}
