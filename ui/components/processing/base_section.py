from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QPushButton,
    QGroupBox
)



class BaseProcessingSection(QGroupBox):


    def __init__(
        self,
        title
    ):

        super().__init__()


        self.checkbox = QCheckBox(
            title
        )


        self.content = QWidget()


        self.setup_ui()



    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        header = QHBoxLayout()


        button = QPushButton(
            "▼"
        )


        button.setFixedWidth(
            30
        )


        header.addWidget(
            self.checkbox
        )


        header.addStretch()


        header.addWidget(
            button
        )


        layout.addLayout(
            header
        )



        layout.addWidget(
            self.content
        )


        self.content.hide()



        button.clicked.connect(
            self.toggle
        )


        self.setLayout(
            layout
        )



    def toggle(
        self
    ):


        self.content.setVisible(
            not self.content.isVisible()
        )



    def enabled(
        self
    ):


        return self.checkbox.isChecked()



    def set_content_layout(
        self,
        layout
    ):


        self.content.setLayout(
            layout
        )