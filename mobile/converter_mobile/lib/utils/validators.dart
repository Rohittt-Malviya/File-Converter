class Validators {
  const Validators._();

  static bool isSupportedExtension(String extension) {
    return {
      'txt',
      'md',
      'csv',
      'json',
      'png',
      'jpg',
      'jpeg',
      'webp',
      'pdf',
    }.contains(extension.toLowerCase().replaceFirst('.', ''));
  }

  static String? required(String? value, {String label = 'Value'}) {
    if (value == null || value.trim().isEmpty) return '$label is required.';
    return null;
  }
}
