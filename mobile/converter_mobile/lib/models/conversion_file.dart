class ConversionFile {
  const ConversionFile({
    required this.name,
    required this.bytes,
  });

  final String name;
  final List<int> bytes;

  int get size => bytes.length;

  String get extension {
    final dot = name.lastIndexOf('.');
    return dot == -1 ? '' : name.substring(dot + 1).toLowerCase();
  }
}
