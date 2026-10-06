from PySide6.QtWidgets import QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget


class Sidebar(QWidget):
    def __init__(self):

        super().__init__()

        self.buttons = {}

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(10, 10, 10, 10)

        layout.setSpacing(6)

        # =====================
        # BRAND
        # =====================

        title = QLabel("PIXVAULT")

        title.setObjectName("sidebar_title")

        layout.addWidget(title)

        # =====================
        # HOME
        # =====================

        self.add_section(layout, "HOME")

        self.create_button(layout, "🏠  Home", "home")

        # =====================
        # IMAGE PROCESSING
        # =====================

        self.add_section(layout, "PROCESSING")

        tools = [
            ("⇄  Convert", "convert"),
            ("📦  Compress", "compress"),
            ("↔  Resize", "resize"),
            ("✂  Crop", "crop"),
            ("🔄  Transform", "transform"),
            ("📐  DPI", "dpi"),
            ("🔒  Metadata", "metadata"),
            ("🎨  Color Space", "colorspace"),
            ("◐  Bit Depth", "bitdepth"),
        ]

        for text, key in tools:
            self.create_button(layout, text, key)

        # =====================
        # MANAGEMENT
        # =====================

        self.add_section(layout, "MANAGEMENT")

        self.create_button(layout, "🕘  History", "history")

        # =====================
        # SYSTEM
        # =====================

        self.add_section(layout, "SYSTEM")

        self.create_button(layout, "⚙  Settings", "settings")

        self.create_button(layout, "🔐  Privacy", "privacy")

        layout.addStretch()

        self.setLayout(layout)

    def add_section(self, layout, text):

        label = QLabel(text)

        label.setObjectName("sidebar_section")

        layout.addWidget(label)

    def create_button(self, layout, text, key):

        button = QPushButton(text)

        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        button.setMinimumHeight(34)

        self.buttons[key] = button

        layout.addWidget(button)
