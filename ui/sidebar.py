from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel
)



class Sidebar(QWidget):


    def __init__(
        self
    ):

        super().__init__()


        self.buttons = {}


        self.setup_ui()



    def setup_ui(
        self
    ):


        layout = QVBoxLayout()



        # Header

        title = QLabel(
            "PIXVAULT"
        )


        layout.addWidget(
            title
        )



        # MAIN

        main_label = QLabel(
            "MAIN"
        )


        layout.addWidget(
            main_label
        )



        self.create_button(
            layout,
            "Home",
            "home"
        )



        # PROCESSING

        processing_label = QLabel(
            "PROCESSING"
        )


        layout.addWidget(
            processing_label
        )



        processing_menu = [

            (
                "All Processing",
                "all_processing"
            ),

            (
                "Convert",
                "convert"
            ),

            (
                "Compress",
                "compress"
            ),

            (
                "Resize",
                "resize"
            ),

            (
                "Crop",
                "crop"
            ),

            (
                "Transform",
                "transform"
            ),

            (
                "DPI",
                "dpi"
            ),

            (
                "Metadata",
                "metadata"
            ),

            (
                "Color Space",
                "colorspace"
            ),

            (
                "Bit Depth",
                "bitdepth"
            )

        ]



        for text, key in processing_menu:


            self.create_button(
                layout,
                text,
                key
            )



        # MANAGEMENT


        management_label = QLabel(
            "MANAGEMENT"
        )


        layout.addWidget(
            management_label
        )


        self.create_button(
            layout,
            "History",
            "history"
        )



        # SYSTEM


        system_label = QLabel(
            "SYSTEM"
        )


        layout.addWidget(
            system_label
        )


        self.create_button(
            layout,
            "Settings",
            "settings"
        )


        self.create_button(
            layout,
            "Privacy",
            "privacy"
        )



        layout.addStretch()



        self.setLayout(
            layout
        )



    def create_button(
        self,
        layout,
        text,
        key
    ):


        button = QPushButton(
            text
        )


        self.buttons[key] = button


        layout.addWidget(
            button
        )