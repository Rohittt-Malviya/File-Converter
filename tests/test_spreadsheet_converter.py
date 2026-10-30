from pathlib import Path

import pytest

pytest.importorskip("openpyxl")

from openpyxl import Workbook
from shared.convert.spreadsheet_converter import SpreadsheetConverter


def test_xlsx_to_csv(tmp_path: Path):
    source = tmp_path / "input.xlsx"
    output = tmp_path / "output.csv"
    workbook = Workbook()
    workbook.active.append(["name", "value"])
    workbook.active.append(["test", 1])
    workbook.save(source)
    SpreadsheetConverter().xlsx_to_csv(source, output)
    assert "name,value" in output.read_text(encoding="utf-8")
