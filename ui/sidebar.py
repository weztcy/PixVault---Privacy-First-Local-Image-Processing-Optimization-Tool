from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel
)


class Sidebar(QWidget):

    def __init__(self):
        super().__init__()

        self.buttons = {}

        self.setup_ui()


    def setup_ui(self):

        layout = QVBoxLayout()

        # Title
        title = QLabel("PIXVAULT")
        layout.addWidget(title)


        # Home
        self.create_button(
            layout,
            "Home",
            "home"
        )


        # Section
        tools_label = QLabel("TOOLS")
        layout.addWidget(tools_label)


        # Tools Menu
        tools = [
            ("All Processing", "all_processing"),
            ("Convert", "convert"),
            ("Compress", "compress"),
            ("Resize", "resize"),
            ("Crop", "crop"),
            ("Transform", "transform"),
            ("DPI", "dpi"),
            ("Metadata", "metadata"),
            ("Color Space", "colorspace"),
            ("Bit Depth", "bitdepth"),
        ]


        for text, key in tools:

            self.create_button(
                layout,
                text,
                key
            )


        # Bottom Menu
        layout.addStretch()


        self.create_button(
            layout,
            "History",
            "history"
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


        self.setLayout(layout)



    def create_button(
        self,
        layout,
        text,
        key
    ):

        button = QPushButton(text)

        self.buttons[key] = button

        layout.addWidget(button)