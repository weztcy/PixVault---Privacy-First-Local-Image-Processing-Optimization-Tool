from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class WarningLabel(QLabel):
    def __init__(self, parent=None):

        super().__init__(parent)

        self.setup_ui()

    def setup_ui(self):

        self.setWordWrap(True)

        self.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.setVisible(False)

        self.setObjectName("processing_warning")

    def show_warning(self, message):

        if not message:
            self.clear_warning()

            return

        self.setText(f"⚠ {message}")

        self.setVisible(True)

    def clear_warning(self):

        self.clear()

        self.setVisible(False)

    def has_warning(self):

        return self.isVisible()
