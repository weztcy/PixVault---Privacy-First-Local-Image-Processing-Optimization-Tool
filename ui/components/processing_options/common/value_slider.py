
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSlider,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class ValueSlider(QWidget):
    value_changed = Signal(int)

    def __init__(
        self,
        title,
        minimum,
        maximum,
        value=None,
        parent=None,
    ):
        super().__init__(parent)

        self.minimum = int(minimum)
        self.maximum = int(maximum)

        self.default_value = (
            int(value)
            if value is not None
            else self.minimum
        )

        self.title = str(title)

        self.setObjectName(
            "value_slider_widget"
        )

        self.setup_ui(self.title)
        self.apply_styles()

        self.set_value(
            self.default_value
        )

    # =====================
    # MAIN USER INTERFACE
    # =====================

    def setup_ui(self, title):
        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            0, 0, 0, 0
        )
        self.main_layout.setSpacing(0)

        # =====================
        # MAIN CONTAINER
        # =====================

        self.container = QFrame()

        self.container.setObjectName(
            "value_slider_card"
        )

        self.container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        container_layout = QVBoxLayout(
            self.container
        )

        container_layout.setContentsMargins(
            16, 14, 16, 12
        )

        container_layout.setSpacing(10)

        # =====================
        # HEADER
        # =====================

        header = QHBoxLayout()

        header.setContentsMargins(
            0, 0, 0, 0
        )

        header.setSpacing(12)

        self.title_label = QLabel(title)

        self.title_label.setObjectName(
            "value_slider_title"
        )

        self.title_label.setWordWrap(True)

        self.title_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        # =====================
        # CURRENT VALUE BADGE
        # =====================

        self.value_label = QLabel("0")

        self.value_label.setObjectName(
            "value_slider_badge"
        )

        self.value_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.value_label.setMinimumWidth(52)

        self.value_label.setMinimumHeight(30)

        header.addWidget(
            self.title_label,
            1,
        )

        header.addWidget(
            self.value_label,
            0,
        )

        container_layout.addLayout(
            header
        )

        # =====================
        # PREMIUM SLIDER
        # =====================

        self.slider = QSlider(
            Qt.Orientation.Horizontal
        )

        self.slider.setObjectName(
            "value_slider_control"
        )

        self.slider.setRange(
            self.minimum,
            self.maximum,
        )

        # Synchronize limits with Qt's
        # actual accepted range.

        self.minimum = (
            self.slider.minimum()
        )

        self.maximum = (
            self.slider.maximum()
        )

        self.slider.setMinimumHeight(30)

        self.slider.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.slider.setFocusPolicy(
            Qt.FocusPolicy.StrongFocus
        )

        self.slider.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.slider.setTickPosition(
            QSlider.TickPosition.NoTicks
        )

        self.slider.setAccessibleName(
            self.title
        )

        self.title_label.setBuddy(
            self.slider
        )

        container_layout.addWidget(
            self.slider
        )

        # =====================
        # RANGE INDICATORS
        # =====================

        range_layout = QHBoxLayout()

        range_layout.setContentsMargins(
            2, 0, 2, 0
        )

        range_layout.setSpacing(8)

        self.minimum_label = QLabel(
            str(self.minimum)
        )

        self.minimum_label.setObjectName(
            "value_slider_range"
        )

        self.maximum_label = QLabel(
            str(self.maximum)
        )

        self.maximum_label.setObjectName(
            "value_slider_range"
        )

        self.maximum_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
        )

        range_layout.addWidget(
            self.minimum_label
        )

        range_layout.addStretch()

        range_layout.addWidget(
            self.maximum_label
        )

        container_layout.addLayout(
            range_layout
        )

        # =====================
        # ASSEMBLE COMPONENT
        # =====================

        self.main_layout.addWidget(
            self.container
        )

        # =====================
        # CONNECT SIGNAL
        # =====================

        self.slider.valueChanged.connect(
            self.on_value_changed
        )

        self.update_display(
            self.slider.value()
        )

    # =====================
    # UPDATE VALUE DISPLAY
    # =====================

    def update_display(self, value):
        actual_value = int(value)

        self.value_label.setText(
            str(actual_value)
        )

        self.slider.setToolTip(
            f"{self.title}: {actual_value}"
        )

        self.value_label.setToolTip(
            f"Current value: {actual_value}"
        )

    # =====================
    # VALUE CHANGED
    # =====================

    def on_value_changed(self, value):
        self.update_display(value)

        self.value_changed.emit(
            int(value)
        )

    # =====================
    # GET CURRENT VALUE
    # =====================

    def value(self):
        return self.slider.value()

    # =====================
    # SET CURRENT VALUE
    # =====================

    def set_value(self, value):
        self.slider.setValue(
            int(value)
        )

        # Read the actual value from the
        # slider because Qt may clamp it
        # to the configured range.

        self.update_display(
            self.slider.value()
        )

    # =====================
    # RESET TO DEFAULT
    # =====================

    def reset(self):
        self.set_value(
            self.default_value
        )

    # =====================
    # UPDATE RANGE
    # =====================

    def set_range(
        self,
        minimum,
        maximum,
    ):
        self.slider.setRange(
            int(minimum),
            int(maximum),
        )

        self.minimum = (
            self.slider.minimum()
        )

        self.maximum = (
            self.slider.maximum()
        )

        self.minimum_label.setText(
            str(self.minimum)
        )

        self.maximum_label.setText(
            str(self.maximum)
        )

        # Update display if the slider
        # value was clamped by the new range.

        self.update_display(
            self.slider.value()
        )

    # =====================
    # OPTIONAL DEFAULT UPDATE
    # =====================

    def set_default_value(self, value):
        self.default_value = int(value)

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        self.setStyleSheet(
            """
            /* =========================
               MAIN COMPONENT
            ========================= */

            QWidget#value_slider_widget {
                background: transparent;
                border: none;
            }

            /* =========================
               PREMIUM CONTAINER
            ========================= */

            QFrame#value_slider_card {
                background-color: #1b2940;

                border: 1px solid #304259;
                border-radius: 11px;
            }

            QFrame#value_slider_card:hover {
                background-color: #1e2e45;

                border: 1px solid #426273;
            }

            /* =========================
               TITLE
            ========================= */

            QLabel#value_slider_title {
                background: transparent;
                border: none;

                color: #d5deea;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;
            }

            /* =========================
               CURRENT VALUE BADGE
            ========================= */

            QLabel#value_slider_badge {
                background-color: #173a40;

                color: #5eead4;

                border: 1px solid #28665f;
                border-radius: 8px;

                padding: 5px 10px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 700;
            }

            /* =========================
               SLIDER BASE
            ========================= */

            QSlider#value_slider_control {
                background: transparent;
                border: none;
            }

            /* =========================
               SLIDER TRACK
            ========================= */

            QSlider#value_slider_control::groove:horizontal {
                background-color: #304259;

                height: 6px;

                border: none;
                border-radius: 3px;
            }

            /* =========================
               ACTIVE TRACK
            ========================= */

            QSlider#value_slider_control::sub-page:horizontal {
                background-color: #5eead4;

                border: none;
                border-radius: 3px;
            }

            /* =========================
               INACTIVE TRACK
            ========================= */

            QSlider#value_slider_control::add-page:horizontal {
                background-color: #304259;

                border: none;
                border-radius: 3px;
            }

            /* =========================
               SLIDER HANDLE
            ========================= */

            QSlider#value_slider_control::handle:horizontal {
                background-color: #5eead4;

                border: 3px solid #101b2d;
                border-radius: 11px;

                width: 16px;
                height: 16px;

                margin: -8px 0;
            }

            /* =========================
               HOVER STATE
            ========================= */

            QSlider#value_slider_control::handle:horizontal:hover {
                background-color: #99f6e4;

                border: 3px solid #173a40;
            }

            /* =========================
               PRESSED STATE
            ========================= */

            QSlider#value_slider_control::handle:horizontal:pressed {
                background-color: #2dd4bf;

                border: 3px solid #285d60;
            }

            /* =========================
               KEYBOARD FOCUS
            ========================= */

            QSlider#value_slider_control:focus::handle:horizontal {
                background-color: #99f6e4;

                border: 3px solid #285d60;
            }

            /* =========================
               MINIMUM / MAXIMUM LABELS
            ========================= */

            QLabel#value_slider_range {
                background: transparent;
                border: none;

                color: #64748b;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 500;
            }

            /* =========================
               DISABLED CONTAINER
            ========================= */

            QFrame#value_slider_card:disabled {
                background-color: #151e2d;

                border: 1px solid #253348;
            }

            /* =========================
               DISABLED LABELS
            ========================= */

            QLabel#value_slider_title:disabled {
                color: #64748b;
            }

            QLabel#value_slider_badge:disabled {
                background-color: #202b3b;

                color: #64748b;

                border: 1px solid #354459;
            }

            QLabel#value_slider_range:disabled {
                color: #475569;
            }

            /* =========================
               DISABLED SLIDER
            ========================= */

            QSlider#value_slider_control::groove:horizontal:disabled {
                background-color: #263348;
            }

            QSlider#value_slider_control::sub-page:horizontal:disabled {
                background-color: #42615f;
            }

            QSlider#value_slider_control::add-page:horizontal:disabled {
                background-color: #263348;
            }

            QSlider#value_slider_control::handle:horizontal:disabled {
                background-color: #64748b;

                border: 3px solid #202b3b;
            }
            """
        )
