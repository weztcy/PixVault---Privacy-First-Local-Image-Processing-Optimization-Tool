from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QScrollArea
)


from PySide6.QtCore import (
    Qt
)








class FormatCard(QFrame):


    def __init__(
        self,
        format_name,
        parent=None
    ):

        super().__init__(
            parent
        )


        self.format_name = format_name


        self.setup_ui()








    def setup_ui(
        self
    ):


        self.setObjectName(
            "format_card"
        )


        self.setFixedSize(
            85,
            45
        )


        self.setStyleSheet(
            """
            QFrame#format_card
            {
                border: 1px solid #555;
                border-radius: 10px;
                background-color: transparent;
            }


            QLabel#format_name
            {
                font-weight: bold;
            }
            """
        )



        layout = QVBoxLayout(
            self
        )


        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        layout.setContentsMargins(
            5,
            5,
            5,
            5
        )



        name = QLabel(
            self.format_name
        )


        name.setObjectName(
            "format_name"
        )


        name.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )



        layout.addWidget(
            name
        )









class FormatSupportInfo(QWidget):


    SUPPORT_DATA = {


        "convert": [

            "JPEG",
            "PNG",
            "WEBP",
            "AVIF",
            "GIF",
            "BMP",
            "TIFF",
            "HEIC",
            "HEIF",
            "ICO",
            "SVG"

        ],



        "resize": [

            "JPEG",
            "PNG",
            "WEBP",
            "AVIF",
            "BMP",
            "TIFF",
            "HEIC",
            "HEIF"

        ],



        "crop": [

            "JPEG",
            "PNG",
            "WEBP",
            "BMP",
            "TIFF"

        ],



        "transform": [

            "JPEG",
            "PNG",
            "WEBP",
            "BMP",
            "TIFF"

        ],



        "compression": [

            "JPEG",
            "PNG",
            "WEBP",
            "TIFF"

        ],



        "dpi": [

            "JPEG",
            "PNG",
            "TIFF"

        ],



        "colorspace": [

            "JPEG",
            "PNG",
            "TIFF"

        ],



        "bitdepth": [

            "PNG",
            "TIFF"

        ],



        "metadata": [

            "JPEG",
            "TIFF",
            "HEIC",
            "HEIF"

        ]

    }








    def __init__(
        self,
        processor_name,
        parent=None
    ):


        super().__init__(
            parent
        )


        self.processor_name = (
            processor_name.lower()
        )


        self.setup_ui()








    def setup_ui(
        self
    ):


        main_layout = QVBoxLayout(
            self
        )


        main_layout.setSpacing(
            8
        )


        main_layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )





        title = QLabel(
            "Supported Formats"
        )


        title.setObjectName(
            "support_title"
        )


        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )



        main_layout.addWidget(
            title
        )








        self.scroll_area = QScrollArea()


        self.scroll_area.setWidgetResizable(
            True
        )


        self.scroll_area.setFrameShape(
            QFrame.Shape.NoFrame
        )


        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )


        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )







        container = QWidget()



        self.card_layout = QHBoxLayout(
            container
        )


        self.card_layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        self.card_layout.setSpacing(
            10
        )


        self.card_layout.setContentsMargins(
            10,
            5,
            10,
            5
        )





        self.scroll_area.setWidget(
            container
        )


        main_layout.addWidget(
            self.scroll_area
        )



        self.refresh()








    def refresh(
        self
    ):


        formats = self.SUPPORT_DATA.get(
            self.processor_name,
            []
        )



        for fmt in formats:


            card = FormatCard(
                fmt
            )


            self.card_layout.addWidget(
                card
            )