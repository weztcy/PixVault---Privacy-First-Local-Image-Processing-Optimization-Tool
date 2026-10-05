from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGroupBox
)



class HomePage(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()



    def setup_ui(self):

        layout = QVBoxLayout()


        title = QLabel(
            "PixVault"
        )


        subtitle = QLabel(
            "Local Image Processing Application"
        )


        description = QLabel(
            """
Process your images locally.

Available features:

• Convert image formats
• Resize images
• Crop images
• Compress images
• Transform images
• Manage DPI
• Convert Color Space
• Change Bit Depth
• Remove Metadata
            """
        )


        description.setWordWrap(
            True
        )


        processing_box = QGroupBox(
            "Processing Engine"
        )


        processing_layout = QVBoxLayout()


        processing_layout.addWidget(
            QLabel(
                "Powered by local pipeline processing."
            )
        )


        processing_layout.addWidget(
            QLabel(
                "No image upload. All operations run on your device."
            )
        )


        processing_box.setLayout(
            processing_layout
        )


        layout.addWidget(
            title
        )


        layout.addWidget(
            subtitle
        )


        layout.addWidget(
            description
        )


        layout.addWidget(
            processing_box
        )


        layout.addStretch()


        self.setLayout(
            layout
        )