from pathlib import Path

import pytest

pytest.importorskip("PIL")

from PIL import Image
from shared.convert.image_converter import ImageConverter


def test_png_to_jpg(tmp_path: Path):
    source = tmp_path / "input.png"
    output = tmp_path / "output.jpg"
    Image.new("RGB", (4, 4), "red").save(source)
    result = ImageConverter().convert(source, output, "jpg")
    assert result.bytes_written > 0
    assert output.exists()
