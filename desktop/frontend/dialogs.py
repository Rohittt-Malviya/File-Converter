"""Dialog helpers isolated from the main window."""

from PyQt6.QtWidgets import QMessageBox


def show_error(parent, message: str) -> None:
    QMessageBox.critical(parent, "Conversion error", message)


def show_success(parent, message: str) -> None:
    QMessageBox.information(parent, "Conversion complete", message)
