from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFrame
)


from PySide6.QtCore import Qt




class HomePage(QWidget):


    def __init__(
        self
    ):

        super().__init__()


        self.setup_ui()



    def setup_ui(
        self
    ):


        layout = QVBoxLayout()


        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        layout.setSpacing(
            20
        )



        # =====================
        # TITLE
        # =====================


        title = QLabel(
            "PIXVAULT"
        )


        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        title.setObjectName(
            "home_title"
        )



        subtitle = QLabel(
            "Privacy-first image processing application"
        )


        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )



        # =====================
        # DESCRIPTION
        # =====================


        description = QLabel(
            """
Your images never leave your device.

Process, convert, optimize, and manage
your images locally with full control.
            """
        )


        description.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        description.setWordWrap(
            True
        )



        # =====================
        # PRIVACY BOX
        # =====================


        privacy_box = QFrame()


        privacy_box.setFrameShape(
            QFrame.Shape.StyledPanel
        )


        privacy_layout = QVBoxLayout()


        privacy_title = QLabel(
            "🔒 Local Processing"
        )


        privacy_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )



        privacy_text = QLabel(
            """
✓ No cloud upload

✓ No external processing

✓ Offline capable

✓ Full control of your files
            """
        )


        privacy_text.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )



        privacy_layout.addWidget(
            privacy_title
        )


        privacy_layout.addWidget(
            privacy_text
        )


        privacy_box.setLayout(
            privacy_layout
        )



        # =====================
        # ACTION
        # =====================


        start_button = QPushButton(
            "Start Processing"
        )


        start_button.setMinimumHeight(
            40
        )


        start_button.clicked.connect(
            self.open_processing
        )



        # =====================
        # ADD
        # =====================


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
            privacy_box
        )


        layout.addWidget(
            start_button
        )


        self.setLayout(
            layout
        )



    def open_processing(
        self
    ):

        parent = self.parentWidget()


        while parent:

            if hasattr(
                parent,
                "show_page"
            ):

                parent.show_page(
                    "all_processing"
                )

                return


            parent = parent.parentWidget()