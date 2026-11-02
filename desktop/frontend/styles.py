"""Application stylesheet."""

LIGHT_STYLE = """
QMainWindow, QWidget { background: #f7f9f6; color: #17211b; }
QPushButton { padding: 9px 16px; border-radius: 8px; border: 1px solid #dfe5df; background: white; }
QPushButton#convertButton { background: #c9ef72; border: 0; font-weight: 700; }
QListWidget, QComboBox, QLineEdit { padding: 8px; border: 1px solid #dfe5df; border-radius: 7px; background: white; }
QProgressBar { height: 10px; border: 0; border-radius: 5px; background: #e5ebe4; text-align: center; }
QProgressBar::chunk { border-radius: 5px; background: #9dc94e; }
"""

DARK_STYLE = """
QMainWindow, QWidget { background: #18201b; color: #edf4ed; }
QPushButton, QListWidget, QComboBox, QLineEdit { color: #edf4ed; padding: 8px; border: 1px solid #465148; border-radius: 7px; background: #253129; }
QPushButton#convertButton { color: #203008; background: #c9ef72; border: 0; font-weight: 700; }
QProgressBar { height: 10px; border: 0; border-radius: 5px; background: #39453c; }
QProgressBar::chunk { border-radius: 5px; background: #9dc94e; }
"""
