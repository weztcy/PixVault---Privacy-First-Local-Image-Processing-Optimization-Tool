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

            18

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
Process, convert, optimize, and manage
your images locally.

No cloud upload.
No external processing.
Your files stay on your device.
            """

        )


        description.setAlignment(

            Qt.AlignmentFlag.AlignCenter

        )


        description.setWordWrap(

            True

        )







        # =====================
        # PRIVACY CARD
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
✓ Offline capable

✓ No cloud upload

✓ Full file ownership

✓ Fast local processing

✓ Complete control over output
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
        # FEATURES CARD
        # =====================


        feature_box = QFrame()


        feature_box.setFrameShape(

            QFrame.Shape.StyledPanel

        )



        feature_layout = QVBoxLayout()



        feature_title = QLabel(

            "Available Tools"

        )


        feature_title.setAlignment(

            Qt.AlignmentFlag.AlignCenter

        )



        feature_text = QLabel(

            """
Convert formats

Resize and crop images

Compress files

Transform orientation

Manage DPI and color space

Control metadata and bit depth
            """

        )


        feature_text.setAlignment(

            Qt.AlignmentFlag.AlignCenter

        )


        feature_layout.addWidget(

            feature_title

        )


        feature_layout.addWidget(

            feature_text

        )



        feature_box.setLayout(

            feature_layout

        )







        # =====================
        # WORKFLOW CARD
        # =====================


        workflow = QLabel(

            """
Workflow:

1. Select image

2. Choose operation

3. Configure output

4. Process locally

5. Save result
            """

        )


        workflow.setAlignment(

            Qt.AlignmentFlag.AlignCenter

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
        # ADD WIDGET
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

            feature_box

        )


        layout.addWidget(

            workflow

        )


        layout.addWidget(

            start_button

        )



        layout.addStretch()



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

                    "convert"

                )

                return



            parent = parent.parentWidget()