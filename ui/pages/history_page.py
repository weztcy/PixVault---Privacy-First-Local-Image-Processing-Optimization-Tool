from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class HistoryPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel(
            "History"
        )

        layout.addWidget(label)

        self.setLayout(layout)