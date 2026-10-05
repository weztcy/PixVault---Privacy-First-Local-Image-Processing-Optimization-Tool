from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class SingleToolPage(QWidget):

    def __init__(self, tool_name):

        super().__init__()

        layout = QVBoxLayout()

        label = QLabel(
            tool_name
        )

        layout.addWidget(label)

        self.setLayout(layout)