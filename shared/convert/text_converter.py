"""Plain text conversion operations."""

from __future__ import annotations

from pathlib import Path

from .base_converter import ConversionResult, Converter
from .document_converter import DocumentConverter
from .utils.exceptions import ConversionError


class TextConverter(Converter):
    def to_pdf(self, source: str | Path, destination: str | Path) -> ConversionResult:
        return DocumentConverter(self.progress).text_to_pdf(source, destination)

    def to_docx(self, source: str | Path, destination: str | Path) -> ConversionResult:
        return DocumentConverter(self.progress).text_to_docx(source, destination)

    def markdown_to_html(self, source: str | Path, destination: str | Path) -> ConversionResult:
        return DocumentConverter(self.progress).markdown_to_html(source, destination)

    def html_to_text(self, source: str | Path, destination: str | Path) -> ConversionResult:
        path = self.validate_input(source)
        try:
            from html.parser import HTMLParser
            class TextParser(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.parts: list[str] = []
                def handle_data(self, data: str) -> None:
                    self.parts.append(data)
            parser = TextParser()
            parser.feed(path.read_text(encoding="utf-8", errors="replace"))
            output = Path(destination)
            output.write_text("\n".join(part.strip() for part in parser.parts if part.strip()), encoding="utf-8")
            return self.result(path, output)
        except Exception as exc:
            raise ConversionError(f"Unable to extract HTML text: {exc}") from exc

    @staticmethod
    def read_text(source: str | Path) -> str:
        path = Path(source)
        for encoding in ("utf-8", "utf-16", "cp1252"):
            try:
                return path.read_text(encoding=encoding)
            except UnicodeDecodeError:
                continue
        raise ConversionError(f"Unable to detect text encoding: {path.name}")
