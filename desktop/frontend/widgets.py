"""Small reusable Qt widgets."""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QLabel, QListWidget


class DropList(QListWidget):
    files_dropped = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setMinimumHeight(180)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        self.files_dropped.emit([url.toLocalFile() for url in event.mimeData().urls()])
        event.acceptProposedAction()


class StatusLabel(QLabel):
    def show_message(self, message: str, error: bool = False):
        self.setText(message)
        self.setStyleSheet("color: #b42318;" if error else "color: #4a681c;")
