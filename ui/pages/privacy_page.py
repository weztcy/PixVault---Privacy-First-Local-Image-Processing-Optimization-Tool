from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class PrivacyPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel(
            "Privacy"
        )

        layout.addWidget(label)

        self.setLayout(layout)