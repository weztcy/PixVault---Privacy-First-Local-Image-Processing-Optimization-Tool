from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class PrivacyPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("privacy_page")
        self.setup_ui()
        self.apply_styles()

    # =====================
    # MAIN LAYOUT
    # =====================

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("privacy_scroll")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.container = QWidget()
        self.container.setObjectName("privacy_container")

        self.content_layout = QVBoxLayout(self.container)
        self.content_layout.setContentsMargins(30, 28, 30, 30)
        self.content_layout.setSpacing(22)

        # Header
        self.content_layout.addWidget(self.create_header())

        # Information cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(18)

        cards_layout.addWidget(self.create_local_card(), 1)

        cards_layout.addWidget(self.create_data_card(), 1)

        self.content_layout.addLayout(cards_layout)

        # Lifecycle
        self.content_layout.addWidget(self.create_lifecycle_card())

        # Footer
        self.content_layout.addWidget(self.create_footer())

        self.content_layout.addStretch()

        self.scroll_area.setWidget(self.container)
        main_layout.addWidget(self.scroll_area)

    # =====================
    # COMMON HELPERS
    # =====================

    def create_label(
        self,
        text,
        object_name,
        word_wrap=True,
    ):
        label = QLabel(text)
        label.setObjectName(object_name)
        label.setWordWrap(word_wrap)

        return label

    def create_card(self, object_name="privacy_card"):
        card = QFrame()
        card.setObjectName(object_name)

        card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 7)
        shadow.setColor(QColor(0, 0, 0, 55))

        card.setGraphicsEffect(shadow)

        return card

    def add_check_item(self, layout, text):
        row = QHBoxLayout()
        row.setSpacing(12)

        icon = self.create_label(
            "✓",
            "privacy_check_icon",
            False,
        )
        icon.setFixedSize(28, 28)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = self.create_label(
            text,
            "privacy_item_text",
        )

        row.addWidget(
            icon,
            0,
            Qt.AlignmentFlag.AlignTop,
        )
        row.addWidget(label, 1)

        layout.addLayout(row)

    # =====================
    # HEADER
    # =====================

    def create_header(self):
        card = self.create_card("privacy_hero")

        layout = QHBoxLayout(card)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(24)

        left = QVBoxLayout()
        left.setSpacing(12)

        eyebrow = self.create_label(
            "PRIVACY & SECURITY",
            "privacy_eyebrow",
        )

        title = self.create_label(
            "Your images.\nYour control.",
            "privacy_hero_title",
        )

        description = self.create_label(
            "PixVault is built around local-first "
            "image processing. Your files are "
            "processed directly on your device, "
            "without requiring cloud uploads "
            "or external processing services.",
            "privacy_hero_description",
        )

        left.addWidget(eyebrow)
        left.addWidget(title)
        left.addWidget(description)

        right = QVBoxLayout()
        right.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right.setSpacing(12)

        status = self.create_label(
            "●  LOCAL-FIRST",
            "privacy_status",
            False,
        )
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        shield = self.create_label(
            "◇",
            "privacy_shield",
            False,
        )
        shield.setAlignment(Qt.AlignmentFlag.AlignCenter)

        status_text = self.create_label(
            "Designed for local processing",
            "privacy_status_text",
        )
        status_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        right.addWidget(status)
        right.addWidget(shield)
        right.addWidget(status_text)

        layout.addLayout(left, 3)
        layout.addLayout(right, 2)

        return card

    # =====================
    # LOCAL PROCESSING
    # =====================

    def create_local_card(self):
        card = self.create_card()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(14)

        badge = self.create_label(
            "01 / PROCESSING",
            "privacy_card_badge",
        )

        title = self.create_label(
            "Local Processing",
            "privacy_card_title",
        )

        description = self.create_label(
            "Image processing is designed to run directly on your device.",
            "privacy_card_description",
        )

        layout.addWidget(badge)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(12)

        items = [
            "Image processing runs locally",
            "Processing engines run on your device",
            "No external image transfer required",
            "Works without cloud dependency",
        ]

        for item in items:
            self.add_check_item(layout, item)

        layout.addStretch()

        return card

    # =====================
    # DATA HANDLING
    # =====================

    def create_data_card(self):
        card = self.create_card()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(26, 26, 26, 26)
        layout.setSpacing(14)

        badge = self.create_label(
            "02 / DATA OWNERSHIP",
            "privacy_card_badge",
        )

        title = self.create_label(
            "Data Handling",
            "privacy_card_title",
        )

        description = self.create_label(
            "Maintain control over your source images and output files.",
            "privacy_card_description",
        )

        layout.addWidget(badge)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(12)

        items = [
            "Source images remain under your control",
            "Output files are saved to your selected folder",
            "Processing history is stored locally",
            "You choose the output destination",
        ]

        for item in items:
            self.add_check_item(layout, item)

        layout.addStretch()

        return card

    # =====================
    # FILE LIFECYCLE
    # =====================

    def create_lifecycle_card(self):
        card = self.create_card()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(26, 24, 26, 26)
        layout.setSpacing(18)

        header = QVBoxLayout()
        header.setSpacing(7)

        badge = self.create_label(
            "03 / WORKFLOW",
            "privacy_card_badge",
        )

        title = self.create_label(
            "File Lifecycle",
            "privacy_card_title",
        )

        description = self.create_label(
            "A simple, transparent workflow from source image to final output.",
            "privacy_card_description",
        )

        header.addWidget(badge)
        header.addWidget(title)
        header.addWidget(description)

        layout.addLayout(header)

        # Horizontal workflow

        steps_layout = QHBoxLayout()
        steps_layout.setSpacing(12)

        steps = [
            (
                "01",
                "Select",
                "Choose your source image",
            ),
            (
                "02",
                "Process",
                "Image processing runs locally",
            ),
            (
                "03",
                "Clean Up",
                "Clean temporary processing files",
            ),
            (
                "04",
                "Export",
                "Save to your selected location",
            ),
        ]

        for number, title, description in steps:
            step = self.create_step(
                number,
                title,
                description,
            )
            steps_layout.addWidget(step, 1)

        layout.addLayout(steps_layout)

        return card

    # =====================
    # WORKFLOW STEP
    # =====================

    def create_step(
        self,
        number,
        title,
        description,
    ):
        step = QFrame()
        step.setObjectName("privacy_step")

        layout = QVBoxLayout(step)
        layout.setContentsMargins(16, 18, 16, 18)
        layout.setSpacing(9)

        number_label = self.create_label(
            number,
            "privacy_step_number",
            False,
        )

        title_label = self.create_label(
            title,
            "privacy_step_title",
        )

        description_label = self.create_label(
            description,
            "privacy_step_description",
        )

        layout.addWidget(number_label)
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addStretch()

        return step

    # =====================
    # FOOTER
    # =====================

    def create_footer(self):
        footer = QWidget()

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(2, 6, 2, 6)

        left = self.create_label(
            "PIXVAULT  /  PRIVACY BY DESIGN",
            "privacy_footer_label",
        )

        right = self.create_label(
            "Your device. Your files. Your control.",
            "privacy_footer_text",
        )

        right.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(left)
        layout.addStretch()
        layout.addWidget(right)

        return footer

    # =====================
    # STYLING
    # =====================

    def apply_styles(self):
        self.setStyleSheet(
            """
            QWidget#privacy_page,
            QWidget#privacy_container,
            QScrollArea#privacy_scroll {
                background-color: #0b1120;
                border: none;
            }

            QFrame#privacy_hero {
                background: qlineargradient(
                    x1:0, y1:0,
                    x2:1, y2:1,
                    stop:0 #152e39,
                    stop:0.5 #122638,
                    stop:1 #151e38
                );
                border: 1px solid #294354;
                border-radius: 18px;
            }

            QFrame#privacy_card {
                background-color: #141e30;
                border: 1px solid #29374c;
                border-radius: 16px;
            }

            QFrame#privacy_step {
                background-color: #1b2940;
                border: 1px solid #304259;
                border-radius: 12px;
            }

            QLabel#privacy_eyebrow {
                color: #5eead4;
                font-family: "Segoe UI";
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 2px;
            }

            QLabel#privacy_hero_title {
                color: #f8fafc;
                font-family: "Segoe UI";
                font-size: 34px;
                font-weight: 800;
            }

            QLabel#privacy_hero_description {
                color: #b8c5d5;
                font-family: "Segoe UI";
                font-size: 13px;
            }

            QLabel#privacy_status {
                color: #5eead4;
                background-color: #173e43;
                border: 1px solid #28665f;
                border-radius: 12px;
                padding: 8px 14px;
                font-family: "Segoe UI";
                font-size: 11px;
                font-weight: 700;
            }

            QLabel#privacy_shield {
                color: #5eead4;
                font-size: 70px;
                font-weight: 700;
            }

            QLabel#privacy_status_text {
                color: #9bb4c5;
                font-family: "Segoe UI";
                font-size: 11px;
            }

            QLabel#privacy_card_badge {
                color: #5eead4;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#privacy_card_title {
                color: #f1f5f9;
                font-family: "Segoe UI";
                font-size: 21px;
                font-weight: 700;
            }

            QLabel#privacy_card_description {
                color: #94a3b8;
                font-family: "Segoe UI";
                font-size: 12px;
            }

            QLabel#privacy_check_icon {
                color: #5eead4;
                background-color: #173c3e;
                border: 1px solid #285d56;
                border-radius: 14px;
                font-size: 14px;
                font-weight: 700;
            }

            QLabel#privacy_item_text {
                color: #d5deea;
                font-family: "Segoe UI";
                font-size: 12px;
            }

            QLabel#privacy_step_number {
                color: #5eead4;
                font-family: "Segoe UI";
                font-size: 20px;
                font-weight: 800;
            }

            QLabel#privacy_step_title {
                color: #f1f5f9;
                font-family: "Segoe UI";
                font-size: 14px;
                font-weight: 700;
            }

            QLabel#privacy_step_description {
                color: #94a3b8;
                font-family: "Segoe UI";
                font-size: 11px;
            }

            QLabel#privacy_footer_label {
                color: #64748b;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
            }

            QLabel#privacy_footer_text {
                color: #64748b;
                font-family: "Segoe UI";
                font-size: 10px;
            }

            QScrollBar:vertical {
                background: #0b1120;
                width: 8px;
                margin: 0;
                border: none;
            }

            QScrollBar::handle:vertical {
                background: #334155;
                border-radius: 4px;
                min-height: 35px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
                border: none;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
            """
        )
