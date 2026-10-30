"""Desktop-facing conversion service with a uniform operation interface."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from shared.convert.document_converter import DocumentConverter
from shared.convert.image_converter import ImageConverter
from shared.convert.pdf_converter import PdfConverter
from shared.convert.spreadsheet_converter import SpreadsheetConverter
from shared.convert.text_converter import TextConverter


class DesktopConverter:
    def __init__(self, progress: Callable[[int, str], None] | None = None) -> None:
        self.progress = progress
        self.image = ImageConverter(progress)
        self.pdf = PdfConverter(progress)
        self.document = DocumentConverter(progress)
        self.spreadsheet = SpreadsheetConverter(progress)
        self.text = TextConverter(progress)

    def convert(self, source: str, destination: str, target_format: str):
        source_path = Path(source)
        target = target_format.lower().lstrip(".")
        if target in {"png", "jpg", "jpeg", "webp", "bmp", "tiff"}:
            return self.image.convert(source_path, destination, target)
        if target == "pdf" and source_path.suffix.lower() in {".txt", ".md"}:
            return self.text.to_pdf(source_path, destination)
        if target == "docx" and source_path.suffix.lower() == ".txt":
            return self.text.to_docx(source_path, destination)
        if target == "html" and source_path.suffix.lower() in {".md", ".markdown"}:
            return self.text.markdown_to_html(source_path, destination)
        if target == "txt" and source_path.suffix.lower() in {".html", ".htm"}:
            return self.text.html_to_text(source_path, destination)
        if target == "csv" and source_path.suffix.lower() == ".xlsx":
            return self.spreadsheet.xlsx_to_csv(source_path, destination)
        if target == "xlsx" and source_path.suffix.lower() == ".csv":
            return self.spreadsheet.csv_to_xlsx(source_path, destination)
        if target == "docx" and source_path.suffix.lower() == ".pdf":
            return self.pdf.to_word(source_path, destination)
        raise ValueError(f"Conversion from {source_path.suffix or 'unknown'} to {target} is not supported.")
