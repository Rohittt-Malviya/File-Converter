"""Input signature and extension validation."""

from __future__ import annotations

from pathlib import Path

from .exceptions import InvalidInputError

SIGNATURES = {
    b"%PDF-": "pdf",
    b"\x89PNG\r\n\x1a\n": "png",
    b"\xff\xd8\xff": "jpg",
    b"PK\x03\x04": "zip-based",
}


def detect_signature(source: str | Path) -> str:
    path = Path(source)
    try:
        header = path.read_bytes()[:16]
    except OSError as exc:
        raise InvalidInputError(f"Unable to inspect input: {path.name}") from exc
    for signature, file_type in SIGNATURES.items():
        if header.startswith(signature):
            return file_type
    return "text-or-unknown"


def validate_extension(source: str | Path, allowed: set[str]) -> Path:
    path = Path(source)
    extension = path.suffix.lower().lstrip(".")
    if extension not in {item.lower().lstrip(".") for item in allowed}:
        raise InvalidInputError(f"Unsupported input extension: .{extension or 'none'}")
    return path
