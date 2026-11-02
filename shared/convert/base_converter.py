"""Common conversion contracts and safe output handling."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .utils.exceptions import ConversionError
from .utils.file_utils import ensure_input_file, safe_output_path

ProgressCallback = Callable[[int, str], None]


@dataclass(frozen=True)
class ConversionResult:
    output_path: Path
    source_path: Path
    bytes_written: int


class Converter:
    """Base class with shared validation and non-overwriting semantics."""

    def __init__(self, progress: ProgressCallback | None = None) -> None:
        self.progress = progress or (lambda _percent, _message: None)

    def validate_input(self, source: str | Path) -> Path:
        return ensure_input_file(source)

    def output_path(
        self, source: str | Path, destination: str | Path | None, extension: str
    ) -> Path:
        return safe_output_path(source, destination, extension)

    def report(self, percent: int, message: str) -> None:
        self.progress(max(0, min(100, percent)), message)

    @staticmethod
    def result(source: Path, output: Path) -> ConversionResult:
        if not output.exists() or output.stat().st_size == 0:
            raise ConversionError(f"Conversion did not create a valid output: {output.name}")
        return ConversionResult(output, source, output.stat().st_size)
