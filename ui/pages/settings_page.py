from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel(
            "Settings"
        )

        layout.addWidget(label)

        self.setLayout(layout)