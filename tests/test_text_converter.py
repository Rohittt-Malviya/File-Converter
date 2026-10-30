from pathlib import Path

from shared.convert.text_converter import TextConverter


def test_html_to_text(tmp_path: Path):
    source = tmp_path / "page.html"
    output = tmp_path / "page.txt"
    source.write_text("<h1>Hello</h1><p>World</p>", encoding="utf-8")
    TextConverter().html_to_text(source, output)
    assert output.read_text(encoding="utf-8") == "Hello\nWorld"
