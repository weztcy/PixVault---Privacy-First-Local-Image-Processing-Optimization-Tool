
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Sidebar(QWidget):

    SECTION_SPACING = 24
    BUTTON_SPACING = 6
    HEADER_SPACING = 12

    def __init__(self):
        super().__init__()

        self.setObjectName("pixvault_sidebar")

        self.buttons = {}

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        self.setup_ui()
        self.apply_styles()

        self.set_active_page("home")

    # =====================
    # MAIN UI
    # =====================

    def setup_ui(self):

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # =====================
        # SCROLL AREA
        # =====================

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("sidebar_scroll")

        self.scroll_area.setWidgetResizable(True)

        self.scroll_area.setFrameShape(
            QFrame.Shape.NoFrame
        )

        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.nav_container = QWidget()
        self.nav_container.setObjectName(
            "sidebar_nav_container"
        )

        layout = QVBoxLayout(self.nav_container)

        layout.setContentsMargins(12, 22, 12, 18)
        layout.setSpacing(self.BUTTON_SPACING)

        # =====================
        # HOME
        # =====================

        self.add_section(
            layout,
            "HOME",
            first=True,
        )

        self.create_button(
            layout,
            "⌂  Home",
            "home",
        )

        # =====================
        # IMAGE PROCESSING
        # =====================

        self.add_section(
            layout,
            "PROCESSING",
        )

        tools = [
            ("⇄  Convert", "convert"),
            ("▣  Compress", "compress"),
            ("↔  Resize", "resize"),
            ("✂  Crop", "crop"),
            ("⟳  Transform", "transform"),
            ("⊞  DPI", "dpi"),
            ("◇  Metadata", "metadata"),
            ("◈  Color Space", "colorspace"),
            ("◐  Bit Depth", "bitdepth"),
        ]

        for text, key in tools:
            self.create_button(
                layout,
                text,
                key,
            )

        # =====================
        # MANAGEMENT
        # =====================

        self.add_section(
            layout,
            "MANAGEMENT",
        )

        self.create_button(
            layout,
            "◷  History",
            "history",
        )

        # =====================
        # SYSTEM
        # =====================

        self.add_section(
            layout,
            "SYSTEM",
        )

        self.create_button(
            layout,
            "◇  Privacy",
            "privacy",
        )

        layout.addStretch()

        self.scroll_area.setWidget(
            self.nav_container
        )

        main_layout.addWidget(
            self.scroll_area,
            1,
        )

        # =====================
        # FOOTER
        # =====================

        footer = self.create_footer()

        main_layout.addWidget(footer)

    # =====================
    # SECTION HEADER
    # =====================

    def add_section(
        self,
        layout,
        text,
        first=False,
    ):

        if not first:
            layout.addSpacing(
                self.SECTION_SPACING
                - self.BUTTON_SPACING
            )

        label = QLabel(text)

        label.setObjectName(
            "sidebar_section"
        )

        label.setAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )

        label.setContentsMargins(
            12, 0, 0, 0
        )

        layout.addWidget(label)

        layout.addSpacing(
            self.HEADER_SPACING
            - self.BUTTON_SPACING
        )

    # =====================
    # NAVIGATION BUTTON
    # =====================

    def create_button(
        self,
        layout,
        text,
        key,
    ):

        button = QPushButton(text)

        button.setObjectName(
            "sidebar_nav_button"
        )

        button.setProperty(
            "page_key",
            key,
        )

        button.setCheckable(True)

        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        button.setMinimumHeight(42)

        button.setFocusPolicy(
            Qt.FocusPolicy.StrongFocus
        )

        self.button_group.addButton(
            button
        )

        self.buttons[key] = button

        layout.addWidget(button)

        return button

    # =====================
    # ACTIVE NAVIGATION
    # =====================

    def set_active_page(
        self,
        page_name,
    ):

        button = self.buttons.get(
            page_name
        )

        if button is not None:
            button.setChecked(True)

    # =====================
    # WORKSPACE SYNC
    # =====================

    def bind_workspace(
        self,
        workspace,
    ):

        workspace.currentChanged.connect(
            lambda index: self.sync_workspace(
                workspace
            )
        )

        self.sync_workspace(workspace)

    def sync_workspace(
        self,
        workspace,
    ):

        current_widget = (
            workspace.currentWidget()
        )

        for name, page in workspace.pages.items():

            if page is current_widget:
                self.set_active_page(name)
                return

    # =====================
    # FOOTER
    # =====================

    def create_footer(self):

        footer_container = QWidget()

        footer_container.setObjectName(
            "sidebar_footer_container"
        )

        outer_layout = QVBoxLayout(
            footer_container
        )

        outer_layout.setContentsMargins(
            12, 12, 12, 16
        )

        outer_layout.setSpacing(0)

        footer = QFrame()

        footer.setObjectName(
            "sidebar_footer_card"
        )

        footer_layout = QVBoxLayout(
            footer
        )

        footer_layout.setContentsMargins(
            14, 12, 14, 12
        )

        footer_layout.setSpacing(6)

        # Status

        status_layout = QHBoxLayout()
        status_layout.setSpacing(8)

        indicator = QLabel("●")

        indicator.setObjectName(
            "sidebar_status_indicator"
        )

        status = QLabel(
            "LOCAL PROCESSING"
        )

        status.setObjectName(
            "sidebar_status_title"
        )

        status_layout.addWidget(
            indicator
        )

        status_layout.addWidget(
            status
        )

        status_layout.addStretch()

        # Description

        description = QLabel(
            "Your files stay on your device"
        )

        description.setObjectName(
            "sidebar_footer_description"
        )

        description.setWordWrap(True)

        footer_layout.addLayout(
            status_layout
        )

        footer_layout.addWidget(
            description
        )

        outer_layout.addWidget(
            footer
        )

        return footer_container

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):

        self.setStyleSheet(
            """
            /* =========================
               SIDEBAR BACKGROUND
            ========================= */

            QWidget#pixvault_sidebar {
                background-color: #0f1728;
                border-right: 1px solid #26364b;
            }

            QWidget#sidebar_nav_container,
            QWidget#sidebar_footer_container {
                background-color: #0f1728;
            }

            QScrollArea#sidebar_scroll {
                background-color: #0f1728;
                border: none;
            }

            /* =========================
               SECTION LABEL
            ========================= */

            QLabel#sidebar_section {
                color: #64748b;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
                background: transparent;
                border: none;
            }

            /* =========================
               NAVIGATION BUTTON
            ========================= */

            QPushButton#sidebar_nav_button {
                background-color: transparent;

                color: #a7b5c9;

                border: 1px solid transparent;
                border-left: 3px solid transparent;

                border-radius: 9px;

                text-align: left;

                padding-left: 14px;
                padding-right: 8px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 500;
            }

            /* =========================
               HOVER
            ========================= */

            QPushButton#sidebar_nav_button:hover:!checked {
                background-color: #1b2b40;

                color: #f1f5f9;

                border: 1px solid #304259;
                border-left: 3px solid transparent;
            }

            /* =========================
               ACTIVE PAGE
            ========================= */

            QPushButton#sidebar_nav_button:checked {
                background-color: #173a40;

                color: #5eead4;

                border: 1px solid #285d60;
                border-left: 3px solid #5eead4;

                font-weight: 700;
            }

            QPushButton#sidebar_nav_button:checked:hover {
                background-color: #1c4649;
                color: #99f6e4;
            }

            /* =========================
               PRESSED
            ========================= */

            QPushButton#sidebar_nav_button:pressed {
                background-color: #244b52;
            }

            /* =========================
               KEYBOARD FOCUS
            ========================= */

            QPushButton#sidebar_nav_button:focus:!checked {
                border: 1px solid #5eead4;
                border-left: 3px solid #5eead4;
            }

            /* =========================
               FOOTER
            ========================= */

            QFrame#sidebar_footer_card {
                background-color: #142b35;

                border: 1px solid #294d51;

                border-radius: 12px;
            }

            QLabel#sidebar_status_indicator {
                color: #5eead4;

                font-family: "Segoe UI";
                font-size: 10px;

                background: transparent;
                border: none;
            }

            QLabel#sidebar_status_title {
                color: #5eead4;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;

                background: transparent;
                border: none;
            }

            QLabel#sidebar_footer_description {
                color: #94a3b8;

                font-family: "Segoe UI";
                font-size: 10px;

                background: transparent;
                border: none;
            }

            /* =========================
               SCROLLBAR
            ========================= */

            QScrollBar:vertical {
                background: #0f1728;

                width: 5px;

                margin: 0;
                border: none;
            }

            QScrollBar::handle:vertical {
                background: #334155;

                border-radius: 2px;

                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: #5eead4;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
                border: none;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }
            """
        )
