from pathlib import Path

from PIL import Image
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.styles.pixvault_theme import apply_page_theme, role


class ImageInfoPanel(QWidget):
    """Image properties panel that grows naturally; no nested QScrollArea."""

    def __init__(self):
        super().__init__()

        self.current_image = None
        self.setObjectName("image_info_panel")
        role(self, "detailPanel")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )
        self.setMinimumWidth(0)

        self.setup_ui()
        self.apply_styles()
        self.clear()

    def label(self, text, kind, wrap=False):
        widget = role(QLabel(str(text)), kind)
        widget.setWordWrap(wrap)
        widget.setTextFormat(Qt.TextFormat.PlainText)
        widget.setMinimumWidth(0)
        return widget

    def setup_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(20, 19, 20, 19)
        main.setSpacing(14)

        # Header and status
        header = QHBoxLayout()
        header.setSpacing(9)

        heading = QVBoxLayout()
        heading.setSpacing(5)
        heading.addWidget(self.label("IMAGE INSPECTOR", "eyebrow"))
        heading.addWidget(self.label("Image Details", "cardTitle"))
        heading.addWidget(
            self.label("Properties of the selected image", "description", True)
        )

        self.status_label = self.label("NO IMAGE", "statusBadge")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setProperty("state", "empty")

        header.addLayout(heading, 1)
        header.addWidget(self.status_label, 0, Qt.AlignmentFlag.AlignTop)
        main.addLayout(header)

        # Retain the original public info_box attribute.
        # Unlike the old version, it does not contain any scroll area.
        self.info_box = role(QGroupBox(), "infoBody")
        body = QVBoxLayout(self.info_box)
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(12)

        body.addWidget(self.label("FILE OVERVIEW", "fieldTitle"))
        self.name_label = self.label("-", "filename", True)
        self.name_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        body.addWidget(self.name_label)
        body.addWidget(self.divider())

        # Three compact values. They expand vertically when text wraps.
        stats = QHBoxLayout()
        stats.setSpacing(9)
        format_card, self.format_label = self.value_card("FORMAT")
        size_card, self.size_label = self.value_card("FILE SIZE")
        res_card, self.resolution_label = self.value_card("RESOLUTION")
        stats.addWidget(format_card, 1)
        stats.addWidget(size_card, 1)
        stats.addWidget(res_card, 1)
        body.addLayout(stats)

        body.addWidget(self.label("IMAGE PROPERTIES", "fieldTitle"))
        properties = QHBoxLayout()
        properties.setSpacing(9)
        mode_card, self.mode_label = self.value_card("COLOR MODE")
        depth_card, self.depth_label = self.value_card("BIT DEPTH / CHANNEL")
        properties.addWidget(mode_card, 1)
        properties.addWidget(depth_card, 1)
        body.addLayout(properties)
        body.addWidget(self.divider())

        # File path with copy functionality
        path_header = QHBoxLayout()
        path_header.setSpacing(10)
        path_header.addWidget(self.label("FILE LOCATION", "fieldTitle"))
        path_header.addStretch()

        self.copy_button = role(QPushButton("Copy Path"), "secondaryButton")
        self.copy_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_button.setEnabled(False)
        self.copy_button.clicked.connect(self.copy_path)
        path_header.addWidget(self.copy_button)
        body.addLayout(path_header)

        path_card = role(QFrame(), "pathCard")
        path_layout = QVBoxLayout(path_card)
        path_layout.setContentsMargins(12, 11, 12, 11)
        self.path_label = self.label("-", "pathValue", True)
        self.path_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        path_layout.addWidget(self.path_label)
        body.addWidget(path_card)

        self.error_label = self.label("", "errorText", True)
        body.addWidget(self.error_label)
        self.error_label.hide()

        main.addWidget(self.info_box)
        main.addStretch(0)

    def value_card(self, title):
        card = role(QFrame(), "miniCard")
        card.setMinimumWidth(0)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 11, 10, 11)
        layout.setSpacing(7)

        title_label = self.label(title, "miniTitle", True)
        value_label = self.label("-", "miniValue", True)
        value_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch(0)
        return card, value_label

    def divider(self):
        line = role(QFrame(), "divider")
        line.setFixedHeight(1)
        return line

    def set_status(self, state, text):
        self.status_label.setText(str(text))
        self.status_label.setProperty("state", str(state))
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
        self.status_label.update()

    def set_image(self, image_path):
        if not image_path:
            self.clear()
            return

        self.current_image = Path(image_path).expanduser()
        self.load_information()

    def load_information(self):
        if self.current_image is None:
            return

        file = self.current_image
        self.reset_information()
        self.name_label.setText(file.name)
        self.path_label.setText(str(file))
        self.path_label.setToolTip(str(file))
        self.copy_button.setEnabled(True)

        try:
            if not file.is_file():
                raise FileNotFoundError("The selected image file does not exist.")

            self.size_label.setText(self.format_size(file.stat().st_size))
            with Image.open(file) as image:
                self.format_label.setText(
                    str(image.format or file.suffix.lstrip(".") or "Unknown").upper()
                )
                self.resolution_label.setText(
                    f"{image.width:,} × {image.height:,}"
                )
                self.mode_label.setText(str(image.mode))
                self.depth_label.setText(self.get_bit_depth(image))

            self.set_status("loaded", "IMAGE LOADED")
        except Exception as error:
            self.show_error(str(error))

    def show_error(self, message):
        self.set_status("error", "UNAVAILABLE")
        self.error_label.setText(f"Unable to read image: {message}")
        self.error_label.show()

    def get_bit_depth(self, image):
        mode = str(image.mode)
        if mode.startswith("I;16"):
            return "16 bit"
        depths = {
            "1": 1, "L": 8, "LA": 8, "P": 8, "PA": 8,
            "RGB": 8, "RGBA": 8, "RGBX": 8, "CMYK": 8,
            "YCbCr": 8, "HSV": 8, "LAB": 8, "I": 32, "F": 32,
        }
        depth = depths.get(mode)
        return f"{depth} bit" if depth is not None else "Unknown"

    def format_size(self, size):
        value = float(size)
        for unit in ("B", "KB", "MB", "GB"):
            if value < 1024:
                return f"{value:.2f} {unit}"
            value /= 1024
        return f"{value:.2f} TB"

    def copy_path(self):
        if self.current_image is None:
            return
        QApplication.clipboard().setText(str(self.current_image))
        self.copy_button.setText("Copied ✓")

    def reset_information(self):
        for label in (
            self.name_label,
            self.path_label,
            self.format_label,
            self.size_label,
            self.resolution_label,
            self.mode_label,
            self.depth_label,
        ):
            label.setText("-")
        self.path_label.setToolTip("")
        self.error_label.clear()
        self.error_label.hide()
        self.copy_button.setEnabled(False)
        self.copy_button.setText("Copy Path")

    def clear(self):
        self.current_image = None
        self.reset_information()
        self.set_status("empty", "NO IMAGE")

    # Existing styling hook retained for compatibility.
    def apply_styles(self):
        apply_page_theme(self)
