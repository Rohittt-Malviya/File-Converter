"""Filesystem safety helpers."""

from __future__ import annotations

import re
from pathlib import Path

from .exceptions import InvalidInputError


def ensure_input_file(source: str | Path) -> Path:
    path = Path(source).expanduser()
    if not path.exists():
        raise InvalidInputError(f"Input file does not exist: {path.name}")
    if not path.is_file():
        raise InvalidInputError(f"Input is not a file: {path.name}")
    if path.stat().st_size == 0:
        raise InvalidInputError(f"Input file is empty: {path.name}")
    return path.resolve()


def sanitize_filename(name: str) -> str:
    clean = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(name).name).strip("._")
    return clean or "converted-file"


def safe_output_path(source: str | Path, destination: str | Path | None, extension: str) -> Path:
    source_path = Path(source)
    if destination:
        output = Path(destination).expanduser()
    else:
        output = source_path.with_name(f"{source_path.stem}-converted.{extension.lstrip('.')}")
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError(f"Output already exists: {output.name}")
    return output
