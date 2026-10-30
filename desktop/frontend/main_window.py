"""Main PyQt6 desktop window."""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QFileDialog, QHBoxLayout, QLabel, QMainWindow, QPushButton, QComboBox,
    QProgressBar, QVBoxLayout, QWidget
)

from desktop.backend.desktop_converter import DesktopConverter
from .dialogs import show_error, show_success
from .styles import DARK_STYLE, LIGHT_STYLE
from .widgets import DropList, StatusLabel


class ConversionWorker(QThread):
    progress = pyqtSignal(int, str)
    completed = pyqtSignal(object)
    failed = pyqtSignal(str)

    def __init__(self, source: str, destination: str, target: str):
        super().__init__()
        self.source, self.destination, self.target = source, destination, target

    def run(self):
        try:
            result = DesktopConverter(self.progress.emit).convert(self.source, self.destination, self.target)
            self.completed.emit(result)
        except Exception as exc:
            self.failed.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local Convert")
        self.resize(760, 560)
        self.files: list[str] = []
        self.history: list[str] = []
        self.worker: ConversionWorker | None = None
        self.dark = False
        self._build_ui()
        self.setStyleSheet(LIGHT_STYLE)

    def _build_ui(self):
        root = QWidget()
        layout = QVBoxLayout(root)
        title = QLabel("<h1>Local Convert</h1><p>Private file conversion on your device.</p>")
        layout.addWidget(title)
        self.file_list = DropList()
        self.file_list.files_dropped.connect(self.add_files)
        layout.addWidget(self.file_list)
        controls = QHBoxLayout()
        browse = QPushButton("Browse files")
        browse.clicked.connect(self.browse)
        controls.addWidget(browse)
        self.format_box = QComboBox()
        self.format_box.addItems(["png", "jpg", "webp", "pdf", "docx", "csv", "xlsx", "txt", "html"])
        controls.addWidget(self.format_box)
        self.theme_button = QPushButton("Dark theme")
        self.theme_button.clicked.connect(self.toggle_theme)
        controls.addWidget(self.theme_button)
        layout.addLayout(controls)
        self.output_label = QLabel("Output folder: beside the source file")
        layout.addWidget(self.output_label)
        self.convert_button = QPushButton("Convert")
        self.convert_button.setObjectName("convertButton")
        self.convert_button.clicked.connect(self.convert)
        layout.addWidget(self.convert_button)
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        self.status = StatusLabel("Drop files above to begin.")
        layout.addWidget(self.status)
        history_label = QLabel("<b>Recent conversions</b>")
        layout.addWidget(history_label)
        self.history_label = QLabel("No conversions yet.")
        layout.addWidget(self.history_label)
        self.setCentralWidget(root)

    def browse(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Choose files")
        self.add_files(files)

    def add_files(self, files: list[str]):
        self.files = list(dict.fromkeys(self.files + [str(Path(path)) for path in files]))
        self.file_list.clear()
        self.file_list.addItems([Path(path).name for path in self.files])
        self.status.show_message(f"{len(self.files)} file(s) ready.")

    def toggle_theme(self):
        self.dark = not self.dark
        self.setStyleSheet(DARK_STYLE if self.dark else LIGHT_STYLE)
        self.theme_button.setText("Light theme" if self.dark else "Dark theme")

    def convert(self):
        if not self.files:
            self.status.show_message("Choose at least one file.", True)
            return
        if len(self.files) > 1:
            self.status.show_message("Convert one file at a time in the desktop app.", True)
            return
        source = self.files[0]
        target = self.format_box.currentText()
        destination, _ = QFileDialog.getSaveFileName(self, "Save converted file", str(Path(source).with_suffix(f".{target}")))
        if not destination:
            return
        self.convert_button.setEnabled(False)
        self.worker = ConversionWorker(source, destination, target)
        self.worker.progress.connect(lambda percent, message: (self.progress.setValue(percent), self.status.show_message(message)))
        self.worker.completed.connect(self._success)
        self.worker.failed.connect(self._failure)
        self.worker.start()

    def _success(self, result):
        self.convert_button.setEnabled(True)
        self.history.insert(0, result.output_path.name)
        self.history_label.setText("\n".join(self.history[:8]))
        show_success(self, f"Created {result.output_path.name}")

    def _failure(self, message: str):
        self.convert_button.setEnabled(True)
        self.status.show_message(message, True)
        show_error(self, message)
