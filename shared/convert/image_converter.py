"""Image conversion, resizing, compression, and PDF export."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .base_converter import ConversionResult, Converter
from .utils.exceptions import ConversionError, UnsupportedConversionError


class ImageConverter(Converter):
    def _open(self, source: str | Path):
        path = self.validate_input(source)
        try:
            from PIL import Image
            image = Image.open(path)
            image.verify()
            image = Image.open(path)
            return path, image
        except Exception as exc:
            raise ConversionError(f"Unable to read image: {path.name}") from exc

    def convert(
        self,
        source: str | Path,
        destination: str | Path | None = None,
        output_format: str = "png",
        quality: int = 90,
    ) -> ConversionResult:
        source_path, image = self._open(source)
        format_name = output_format.lower().replace("jpg", "jpeg")
        if format_name not in {"png", "jpeg", "webp", "bmp", "tiff"}:
            raise UnsupportedConversionError(f"Unsupported image output: {output_format}")
        extension = "jpg" if format_name == "jpeg" else format_name
        output = self.output_path(source_path, destination, extension)
        try:
            if format_name in {"jpeg", "bmp"} and image.mode not in {"RGB", "L"}:
                image = image.convert("RGB")
            options = {"quality": max(1, min(100, quality))} if format_name in {"jpeg", "webp"} else {}
            image.save(output, format_name.upper(), **options)
            return self.result(source_path, output)
        except Exception as exc:
            raise ConversionError(f"Unable to convert image: {exc}") from exc
        finally:
            image.close()

    def resize(self, source: str | Path, destination: str | Path, width: int, height: int | None = None) -> ConversionResult:
        source_path, image = self._open(source)
        if width <= 0 or (height is not None and height <= 0):
            raise ConversionError("Image dimensions must be positive.")
        output = Path(destination)
        try:
            if height is None:
                height = round(image.height * width / image.width)
            resized = image.resize((width, height))
            resized.save(output)
            resized.close()
            return self.result(source_path, output)
        finally:
            image.close()

    def rotate(self, source: str | Path, destination: str | Path, degrees: int) -> ConversionResult:
        source_path, image = self._open(source)
        try:
            image.rotate(degrees, expand=True).save(destination)
            return self.result(source_path, Path(destination))
        finally:
            image.close()

    def images_to_pdf(self, sources: Iterable[str | Path], destination: str | Path) -> ConversionResult:
        paths = [self.validate_input(path) for path in sources]
        if not paths:
            raise ConversionError("At least one image is required.")
        try:
            from PIL import Image
            images = [Image.open(path).convert("RGB") for path in paths]
            output = Path(destination)
            output.parent.mkdir(parents=True, exist_ok=True)
            images[0].save(output, "PDF", save_all=True, append_images=images[1:])
            for image in images:
                image.close()
            return self.result(paths[0], output)
        except Exception as exc:
            raise ConversionError(f"Unable to create PDF: {exc}") from exc
