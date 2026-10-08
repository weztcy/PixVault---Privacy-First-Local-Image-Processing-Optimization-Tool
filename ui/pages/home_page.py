from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QBoxLayout,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.setObjectName("home_page")

        self.setup_ui()
        self.apply_styles()

    # =====================
    # MAIN UI
    # =====================

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scroll Area

        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("home_scroll")

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        # Container

        self.container = QWidget()
        self.container.setObjectName("home_container")

        self.content_layout = QVBoxLayout(self.container)

        self.content_layout.setContentsMargins(28, 26, 28, 26)

        self.content_layout.setSpacing(20)

        # =====================
        # TOP CONTENT
        # =====================

        self.top_layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)

        self.top_layout.setSpacing(18)

        self.hero_card = self.create_hero_card()
        self.privacy_card = self.create_privacy_card()
        self.features_card = self.create_features_card()

        self.top_layout.addWidget(self.hero_card, 5)

        self.top_layout.addWidget(self.privacy_card, 4)

        self.top_layout.addWidget(self.features_card, 5)

        self.content_layout.addLayout(self.top_layout, 1)

        # =====================
        # WORKFLOW
        # =====================

        self.workflow_card = self.create_workflow_card()

        self.content_layout.addWidget(self.workflow_card)

        # =====================
        # FOOTER
        # =====================

        self.content_layout.addWidget(self.create_footer())

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

    def create_card(
        self,
        object_name="home_card",
    ):
        card = QFrame()

        card.setObjectName(object_name)

        card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        card.setMinimumHeight(405)

        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(26)
        shadow.setOffset(0, 6)

        shadow.setColor(QColor(0, 0, 0, 50))

        card.setGraphicsEffect(shadow)

        return card

    # =====================
    # HERO CARD
    # =====================

    def create_hero_card(self):
        card = self.create_card("home_hero_card")

        layout = QVBoxLayout(card)

        layout.setContentsMargins(26, 28, 26, 26)

        layout.setSpacing(12)

        # Badge

        badge = self.create_label(
            "PRIVACY-FIRST IMAGE PROCESSING",
            "home_eyebrow",
        )

        # Main Title

        title = self.create_label(
            "PIXVAULT",
            "home_hero_title",
        )

        subtitle = self.create_label(
            "Powerful image processing.\nComplete local control.",
            "home_hero_subtitle",
        )

        # Description

        description = self.create_label(
            "Convert, resize, crop, compress, "
            "and optimize your images directly "
            "on your device.",
            "home_hero_description",
        )

        privacy_note = self.create_label(
            "No cloud uploads required. Your images remain under your control.",
            "home_hero_note",
        )

        # Action Button

        start_button = QPushButton("Start Processing   →")

        start_button.setObjectName("home_start_button")

        start_button.setMinimumHeight(48)

        start_button.setCursor(Qt.CursorShape.PointingHandCursor)

        start_button.clicked.connect(self.open_processing)

        # Layout

        layout.addWidget(badge)
        layout.addSpacing(14)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(12)
        layout.addWidget(description)
        layout.addWidget(privacy_note)

        layout.addStretch()

        layout.addWidget(start_button)

        return card

    # =====================
    # PRIVACY CARD
    # =====================

    def create_privacy_card(self):
        card = self.create_card("home_card")

        layout = QVBoxLayout(card)

        layout.setContentsMargins(24, 26, 24, 26)

        layout.setSpacing(13)

        badge = self.create_label(
            "01 / PRIVACY",
            "home_card_badge",
        )

        title = self.create_label(
            "Local Processing",
            "home_card_title",
        )

        description = self.create_label(
            "Built around privacy, local processing, and file ownership.",
            "home_card_description",
        )

        layout.addWidget(badge)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(12)

        features = [
            "Offline capable",
            "No cloud upload required",
            "Full file ownership",
            "Local image processing",
            "Complete control over output",
        ]

        for feature in features:
            self.add_privacy_row(
                layout,
                feature,
            )

        layout.addStretch()

        return card

    # =====================
    # PRIVACY ITEM
    # =====================

    def add_privacy_row(
        self,
        layout,
        text,
    ):
        row = QHBoxLayout()
        row.setSpacing(11)

        icon = self.create_label(
            "✓",
            "home_check_icon",
            False,
        )

        icon.setFixedSize(27, 27)

        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label = self.create_label(
            text,
            "home_item_text",
        )

        row.addWidget(
            icon,
            0,
            Qt.AlignmentFlag.AlignTop,
        )

        row.addWidget(label, 1)

        layout.addLayout(row)

    # =====================
    # FEATURES CARD
    # =====================

    def create_features_card(self):
        card = self.create_card("home_card")

        layout = QVBoxLayout(card)

        layout.setContentsMargins(22, 26, 22, 26)

        layout.setSpacing(12)

        badge = self.create_label(
            "02 / TOOLKIT",
            "home_card_badge",
        )

        title = self.create_label(
            "Available Tools",
            "home_card_title",
        )

        description = self.create_label(
            "Everything you need to prepare and optimize your images.",
            "home_card_description",
        )

        layout.addWidget(badge)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(8)

        # =====================
        # TWO-COLUMN TOOL GRID
        # =====================

        tools_grid = QGridLayout()
        tools_grid.setSpacing(8)

        tools = [
            ("⇄", "Convert Images to Different Formats"),
            ("▣", "Compress Images to Reduce File Size"),
            ("↔", "Resize Images to Custom Dimensions"),
            ("✂", "Crop Images to Selected Areas"),
            ("⟳", "Rotate, Flip, and Transform Images"),
            ("▦", "Adjust Image DPI and Resolution"),
            ("◇", "Manage and Remove Image Metadata"),
            ("◈", "Convert and Manage Image Color Space"),
            ("◐", "Adjust Image Bit Depth to Various Levels"),
        ]

        for index, (symbol, name) in enumerate(tools):
            row = index // 1
            column = index % 1

            tool_card = self.create_tool_item(
                symbol,
                name,
            )

            tools_grid.addWidget(
                tool_card,
                row,
                column,
            )

        tools_grid.setColumnStretch(0, 1)
        tools_grid.setColumnStretch(1, 1)

        layout.addLayout(tools_grid)
        layout.addStretch()

        return card

    # =====================
    # TOOL ITEM
    # =====================

    def create_tool_item(
        self,
        symbol,
        text,
    ):
        item = QFrame()
        item.setObjectName("home_tool_item")

        item.setMinimumHeight(38)

        item.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        layout = QHBoxLayout(item)

        layout.setContentsMargins(9, 7, 8, 7)

        layout.setSpacing(7)

        icon = self.create_label(
            symbol,
            "home_tool_icon",
            False,
        )

        icon.setFixedWidth(17)

        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        name = self.create_label(
            text,
            "home_tool_text",
        )

        layout.addWidget(icon)
        layout.addWidget(name, 1)

        return item

    # =====================
    # WORKFLOW CARD
    # =====================

    def create_workflow_card(self):
        card = QFrame()
        card.setObjectName("home_workflow_card")

        layout = QVBoxLayout(card)

        layout.setContentsMargins(24, 22, 24, 24)

        layout.setSpacing(15)

        # Header

        badge = self.create_label(
            "03 / GETTING STARTED",
            "home_card_badge",
        )

        title = self.create_label(
            "Simple Workflow",
            "home_card_title",
        )

        description = self.create_label(
            "From importing your image to exporting the result in five simple steps.",
            "home_card_description",
        )

        layout.addWidget(badge)
        layout.addWidget(title)
        layout.addWidget(description)

        # Horizontal Steps

        steps_layout = QHBoxLayout()
        steps_layout.setSpacing(12)

        steps = [
            (
                "01",
                "Select Image",
                "Import your files",
            ),
            (
                "02",
                "Choose Operation",
                "Select a tool",
            ),
            (
                "03",
                "Configure Output",
                "Adjust options",
            ),
            (
                "04",
                "Process Locally",
                "Run processing",
            ),
            (
                "05",
                "Save Result",
                "Export your image",
            ),
        ]

        for number, title, subtitle in steps:
            step = self.create_workflow_step(
                number,
                title,
                subtitle,
            )

            steps_layout.addWidget(step, 1)

        layout.addLayout(steps_layout)

        return card

    # =====================
    # WORKFLOW STEP
    # =====================

    def create_workflow_step(
        self,
        number,
        title,
        description,
    ):
        step = QFrame()

        step.setObjectName("home_workflow_step")

        layout = QVBoxLayout(step)

        layout.setContentsMargins(12, 14, 12, 14)

        layout.setSpacing(7)

        number_label = self.create_label(
            number,
            "home_step_number",
            False,
        )

        title_label = self.create_label(
            title,
            "home_step_title",
        )

        description_label = self.create_label(
            description,
            "home_step_description",
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
        layout.setContentsMargins(2, 4, 2, 4)

        left = self.create_label(
            "PIXVAULT  /  LOCAL IMAGE STUDIO",
            "home_footer_label",
        )

        right = self.create_label(
            "Your device. Your files. Your control.",
            "home_footer_text",
        )

        right.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout.addWidget(left)
        layout.addStretch()
        layout.addWidget(right)

        return footer

    # =====================
    # RESPONSIVE LAYOUT
    # =====================

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if not hasattr(self, "top_layout"):
            return

        if self.width() < 850:
            self.top_layout.setDirection(QBoxLayout.Direction.TopToBottom)
        else:
            self.top_layout.setDirection(QBoxLayout.Direction.LeftToRight)

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        self.setStyleSheet(
            """
            /* PAGE BACKGROUND */

            QWidget#home_page,
            QWidget#home_container,
            QScrollArea#home_scroll {
                background-color: #0b1120;
                border: none;
            }

            /* HERO CARD */

            QFrame#home_hero_card {
                background: qlineargradient(
                    x1:0, y1:0,
                    x2:1, y2:1,
                    stop:0 #15343b,
                    stop:0.5 #142b3b,
                    stop:1 #17213b
                );

                border: 1px solid #294b54;
                border-radius: 18px;
            }

            /* STANDARD CARDS */

            QFrame#home_card,
            QFrame#home_workflow_card {
                background-color: #141e30;
                border: 1px solid #29374c;
                border-radius: 16px;
            }

            /* TOOL ITEMS */

            QFrame#home_tool_item {
                background-color: #1b2940;
                border: 1px solid #304259;
                border-radius: 9px;
            }

            /* WORKFLOW STEPS */

            QFrame#home_workflow_step {
                background-color: #1b2940;
                border: 1px solid #304259;
                border-radius: 11px;
            }

            /* HERO EYEBROW */

            QLabel#home_eyebrow {
                color: #5eead4;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
                background: transparent;
                border: none;
            }

            /* MAIN TITLE */

            QLabel#home_hero_title {
                color: #f8fafc;
                font-family: "Segoe UI";
                font-size: 34px;
                font-weight: 800;
                background: transparent;
                border: none;
            }

            /* HERO SUBTITLE */

            QLabel#home_hero_subtitle {
                color: #e2e8f0;
                font-family: "Segoe UI";
                font-size: 18px;
                font-weight: 600;
                background: transparent;
                border: none;
            }

            /* HERO DESCRIPTION */

            QLabel#home_hero_description {
                color: #b8c5d5;
                font-family: "Segoe UI";
                font-size: 13px;
                background: transparent;
                border: none;
            }

            QLabel#home_hero_note {
                color: #8da9ad;
                font-family: "Segoe UI";
                font-size: 11px;
                background: transparent;
                border: none;
            }

            /* CARD BADGE */

            QLabel#home_card_badge {
                color: #5eead4;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                letter-spacing: 1px;
                background: transparent;
                border: none;
            }

            /* CARD TITLE */

            QLabel#home_card_title {
                color: #f1f5f9;
                font-family: "Segoe UI";
                font-size: 20px;
                font-weight: 700;
                background: transparent;
                border: none;
            }

            /* CARD DESCRIPTION */

            QLabel#home_card_description {
                color: #94a3b8;
                font-family: "Segoe UI";
                font-size: 12px;
                background: transparent;
                border: none;
            }

            /* CHECK ICON */

            QLabel#home_check_icon {
                color: #5eead4;
                background-color: #173c3e;
                border: 1px solid #285d56;
                border-radius: 13px;
                font-size: 13px;
                font-weight: 700;
            }

            /* PRIVACY ITEM TEXT */

            QLabel#home_item_text {
                color: #d5deea;
                font-family: "Segoe UI";
                font-size: 12px;
                background: transparent;
                border: none;
            }

            /* TOOL ICON */

            QLabel#home_tool_icon {
                color: #5eead4;
                font-family: "Segoe UI";
                font-size: 15px;
                font-weight: 700;
                background: transparent;
                border: none;
            }

            /* TOOL TEXT */

            QLabel#home_tool_text {
                color: #d5deea;
                font-family: "Segoe UI";
                font-size: 11px;
                font-weight: 500;
                background: transparent;
                border: none;
            }

            /* WORKFLOW NUMBER */

            QLabel#home_step_number {
                color: #5eead4;
                font-family: "Segoe UI";
                font-size: 19px;
                font-weight: 800;
                background: transparent;
                border: none;
            }

            /* WORKFLOW TITLE */

            QLabel#home_step_title {
                color: #f1f5f9;
                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 700;
                background: transparent;
                border: none;
            }

            /* WORKFLOW DESCRIPTION */

            QLabel#home_step_description {
                color: #94a3b8;
                font-family: "Segoe UI";
                font-size: 11px;
                background: transparent;
                border: none;
            }

            /* START BUTTON */

            QPushButton#home_start_button {
                background-color: #5eead4;
                color: #0b1120;

                border: none;
                border-radius: 10px;

                padding: 10px 16px;

                font-family: "Segoe UI";
                font-size: 13px;
                font-weight: 700;
            }

            QPushButton#home_start_button:hover {
                background-color: #99f6e4;
            }

            QPushButton#home_start_button:pressed {
                background-color: #2dd4bf;
            }

            /* FOOTER */

            QLabel#home_footer_label {
                color: #64748b;
                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 700;
                background: transparent;
                border: none;
            }

            QLabel#home_footer_text {
                color: #64748b;
                font-family: "Segoe UI";
                font-size: 10px;
                background: transparent;
                border: none;
            }

            /* SCROLLBAR */

            QScrollBar:vertical {
                background: #0b1120;
                width: 7px;
                margin: 0;
                border: none;
            }

            QScrollBar::handle:vertical {
                background: #334155;
                border-radius: 3px;
                min-height: 35px;
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

    # =====================
    # NAVIGATION
    # =====================

    def open_processing(self):
        parent = self.parentWidget()

        while parent is not None:
            if hasattr(parent, "show_page"):
                parent.show_page("convert")
                return

            parent = parent.parentWidget()
