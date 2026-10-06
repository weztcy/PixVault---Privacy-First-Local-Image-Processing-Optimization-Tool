from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGroupBox
)


from PySide6.QtCore import Qt





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


        layout.setSpacing(

            15

        )





        # =====================
        # TITLE
        # =====================


        title = QLabel(

            "Privacy & Security"

        )


        title.setObjectName(

            "privacy_title"

        )


        title.setAlignment(

            Qt.AlignmentFlag.AlignCenter

        )






        # =====================
        # INTRO
        # =====================


        description = QLabel(

            """
PixVault is designed as a local-first image processing application.

Your images are processed directly on your device.
No cloud upload or external processing service is required.

You control the source files, processing options,
and output destination.
            """

        )


        description.setWordWrap(

            True

        )



        description.setAlignment(

            Qt.AlignmentFlag.AlignCenter

        )







        # =====================
        # LOCAL PROCESSING
        # =====================


        local_box = QGroupBox(

            "Local Processing"

        )


        local_box.setObjectName(

            "privacy_card"

        )



        local_layout = QVBoxLayout()



        local_text = QLabel(

            """
✓ Image processing runs locally

✓ Processing engines run on your device

✓ No external image transfer required

✓ Works without cloud dependency
            """

        )


        local_text.setWordWrap(

            True

        )



        local_layout.addWidget(

            local_text

        )


        local_box.setLayout(

            local_layout

        )







        # =====================
        # DATA HANDLING
        # =====================


        data_box = QGroupBox(

            "Data Handling"

        )


        data_box.setObjectName(

            "privacy_card"

        )



        data_layout = QVBoxLayout()



        data_text = QLabel(

            """
Source images remain under your control.

Output files are created only in the folder
selected by the user.

History records are stored locally.
            """

        )


        data_text.setWordWrap(

            True

        )



        data_layout.addWidget(

            data_text

        )


        data_box.setLayout(

            data_layout

        )








        # =====================
        # FILE LIFECYCLE
        # =====================


        lifecycle_box = QGroupBox(

            "File Lifecycle"

        )


        lifecycle_box.setObjectName(

            "privacy_card"

        )



        lifecycle_layout = QVBoxLayout()



        lifecycle_text = QLabel(

            """
1. User selects source image

2. Processing runs locally

3. Temporary processing files are cleaned

4. Final output is saved to selected location
            """

        )


        lifecycle_text.setWordWrap(

            True

        )



        lifecycle_layout.addWidget(

            lifecycle_text

        )


        lifecycle_box.setLayout(

            lifecycle_layout

        )







        # =====================
        # ADD
        # =====================


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


        layout.addWidget(

            lifecycle_box

        )


        layout.addStretch()



        self.setLayout(

            layout

        )