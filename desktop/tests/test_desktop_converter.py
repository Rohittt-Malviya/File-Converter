from pathlib import Path

from desktop.backend.desktop_converter import DesktopConverter


def test_text_to_html(tmp_path: Path):
    source = tmp_path / "note.md"
    destination = tmp_path / "note.html"
    source.write_text("# Hello", encoding="utf-8")
    result = DesktopConverter().convert(str(source), str(destination), "html")
    assert result.output_path == destination
    assert destination.exists()

