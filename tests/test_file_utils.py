from pathlib import Path

import pytest

from shared.convert.utils.exceptions import InvalidInputError
from shared.convert.utils.file_utils import ensure_input_file, sanitize_filename
from shared.convert.utils.validation import detect_signature


def test_safe_file_helpers(tmp_path: Path):
    source = tmp_path / "hello.txt"
    source.write_text("hello", encoding="utf-8")
    assert ensure_input_file(source) == source.resolve()
    assert sanitize_filename("../../hello world.txt") == "hello_world.txt"


def test_missing_and_empty_files_are_rejected(tmp_path: Path):
    with pytest.raises(InvalidInputError):
        ensure_input_file(tmp_path / "missing.txt")
    empty = tmp_path / "empty.txt"
    empty.touch()
    with pytest.raises(InvalidInputError):
        ensure_input_file(empty)


def test_signature_detection(tmp_path: Path):
    source = tmp_path / "file.pdf"
    source.write_bytes(b"%PDF-1.7\n")
    assert detect_signature(source) == "pdf"
