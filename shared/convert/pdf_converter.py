"""PDF conversion operations powered by PyMuPDF and optional pdf2docx."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .base_converter import ConversionResult, Converter
from .utils.exceptions import ConversionError, UnsupportedConversionError


class PdfConverter(Converter):
    def _open(self, source: Path):
        try:
            import fitz
            document = fitz.open(source)
            if document.needs_pass:
                document.close()
                raise UnsupportedConversionError("Password-protected PDFs require an unlocked copy.")
            return document
        except UnsupportedConversionError:
            raise
        except Exception as exc:
            raise ConversionError(f"Unable to read PDF: {exc}") from exc

    def to_images(self, source: str | Path, output_dir: str | Path, image_format: str = "png") -> list[Path]:
        source_path = self.validate_input(source)
        if image_format.lower() not in {"png", "jpg", "jpeg"}:
            raise UnsupportedConversionError("PDF images must be PNG or JPEG.")
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)
        document = self._open(source_path)
        paths: list[Path] = []
        try:
            for index, page in enumerate(document):
                pixmap = page.get_pixmap(matrix=__import__("fitz").Matrix(2, 2), alpha=False)
                path = output / f"{source_path.stem}-page-{index + 1}.{image_format.lower()}"
                pixmap.save(str(path))
                paths.append(path)
                self.report(int((index + 1) / max(1, len(document)) * 100), f"Rendered page {index + 1}")
        finally:
            document.close()
        return paths

    def images_to_pdf(self, sources: Iterable[str | Path], destination: str | Path) -> ConversionResult:
        source_paths = [self.validate_input(path) for path in sources]
        if not source_paths:
            raise ConversionError("At least one image is required.")
        try:
            from PIL import Image
            images = [Image.open(path).convert("RGB") for path in source_paths]
            output = Path(destination)
            output.parent.mkdir(parents=True, exist_ok=True)
            images[0].save(output, save_all=True, append_images=images[1:])
            for image in images:
                image.close()
            return self.result(source_paths[0], output)
        except Exception as exc:
            raise ConversionError(f"Unable to create PDF from images: {exc}") from exc

    def merge(self, sources: Iterable[str | Path], destination: str | Path) -> ConversionResult:
        paths = [self.validate_input(path) for path in sources]
        if not paths:
            raise ConversionError("At least one PDF is required.")
        try:
            import fitz
            output = Path(destination)
            output.parent.mkdir(parents=True, exist_ok=True)
            merged = fitz.open()
            for path in paths:
                document = self._open(path)
                merged.insert_pdf(document)
                document.close()
            merged.save(output)
            merged.close()
            return self.result(paths[0], output)
        except Exception as exc:
            raise ConversionError(f"Unable to merge PDFs: {exc}") from exc

    def split(self, source: str | Path, output_dir: str | Path) -> list[Path]:
        source_path = self.validate_input(source)
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)
        document = self._open(source_path)
        paths: list[Path] = []
        try:
            import fitz
            for index in range(len(document)):
                page_document = fitz.open()
                page_document.insert_pdf(document, from_page=index, to_page=index)
                path = output / f"{source_path.stem}-page-{index + 1}.pdf"
                page_document.save(path)
                page_document.close()
                paths.append(path)
        finally:
            document.close()
        return paths

    def extract_text(self, source: str | Path) -> str:
        source_path = self.validate_input(source)
        document = self._open(source_path)
        try:
            return "\n".join(page.get_text() for page in document)
        finally:
            document.close()

    def metadata(self, source: str | Path) -> dict[str, object]:
        source_path = self.validate_input(source)
        document = self._open(source_path)
        try:
            return dict(document.metadata)
        finally:
            document.close()

    def rotate(self, source: str | Path, destination: str | Path, degrees: int = 90) -> ConversionResult:
        source_path = self.validate_input(source)
        if degrees % 90:
            raise ConversionError("PDF rotation must use a multiple of 90 degrees.")
        document = self._open(source_path)
        output = Path(destination)
        try:
            for page in document:
                page.set_rotation((page.rotation + degrees) % 360)
            document.save(output)
        finally:
            document.close()
        return self.result(source_path, output)

    def to_word(self, source: str | Path, destination: str | Path) -> ConversionResult:
        source_path = self.validate_input(source)
        try:
            from pdf2docx import Converter as PdfToDocx
            output = Path(destination)
            converter = PdfToDocx(str(source_path))
            converter.convert(str(output))
            converter.close()
            return self.result(source_path, output)
        except ImportError as exc:
            raise UnsupportedConversionError("Install pdf2docx for PDF to Word conversion.") from exc
        except Exception as exc:
            raise ConversionError(f"Unable to convert PDF to Word: {exc}") from exc
