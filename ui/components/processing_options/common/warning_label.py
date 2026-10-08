"""A single reusable visual warning used throughout processing options."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class WarningLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("processing_warning")
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.hide()
        self.setStyleSheet("""
            QLabel#processing_warning {
                background-color: #443820; color: #FCD34D;
                border: 1px solid #77602A; border-radius: 8px;
                padding: 10px; font-family: 'Segoe UI'; font-size: 11px;
            }
        """)

    def show_warning(self, message):
        if not message:
            return self.clear_warning()
        self.setText("⚠ " + str(message))
        self.show()

    def clear_warning(self):
        self.clear()
        self.hide()

    def has_warning(self):
        return bool(self.text())
