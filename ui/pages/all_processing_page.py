from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class AllProcessingPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel(
            "All Processing"
        )

        layout.addWidget(label)

        self.setLayout(layout)