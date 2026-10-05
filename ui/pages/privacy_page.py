from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGroupBox
)




class PrivacyPage(QWidget):


    def __init__(
        self
    ):

        super().__init__()


        self.setup_ui()



    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        title = QLabel(
            "Privacy"
        )



        description = QLabel(
            """
PixVault Privacy Information


• All image processing runs locally on your device.

• Images are not uploaded to external servers.

• Output files are created only in your selected folder.

• Metadata cleaning is performed locally.

• You have full control over your source and output files.
            """
        )


        description.setWordWrap(
            True
        )



        local_box = QGroupBox(
            "Local Processing"
        )


        local_layout = QVBoxLayout()


        local_layout.addWidget(
            QLabel(
                "PixVault uses local processing engines "
                "without cloud dependency."
            )
        )


        local_box.setLayout(
            local_layout
        )



        data_box = QGroupBox(
            "Data Handling"
        )


        data_layout = QVBoxLayout()


        data_layout.addWidget(
            QLabel(
                "No image data is transmitted. "
                "History records are stored locally."
            )
        )


        data_box.setLayout(
            data_layout
        )



        layout.addWidget(
            title
        )


        layout.addWidget(
            description
        )


        layout.addWidget(
            local_box
        )


        layout.addWidget(
            data_box
        )


        layout.addStretch()



        self.setLayout(
            layout
        )