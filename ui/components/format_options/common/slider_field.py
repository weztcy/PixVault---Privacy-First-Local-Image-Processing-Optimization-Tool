from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class SliderField(QWidget):
    value_changed = Signal(int)

    def __init__(
        self,
        title,
        minimum,
        maximum,
        default,
    ):
        super().__init__()

        self.setObjectName("slider_field")

        self.title = title

        self.setup_ui(
            minimum,
            maximum,
            default,
        )

        self.apply_styles()

    # =====================
    # USER INTERFACE
    # =====================

    def setup_ui(
        self,
        minimum,
        maximum,
        default,
    ):
        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # =====================
        # FIELD CONTAINER
        # =====================

        self.container = QFrame()
        self.container.setObjectName("slider_field_container")

        self.container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        container_layout = QVBoxLayout(self.container)

        container_layout.setContentsMargins(16, 14, 16, 12)
        container_layout.setSpacing(12)

        # =====================
        # HEADER
        # =====================

        header_layout = QHBoxLayout()

        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(12)

        # Field Title

        self.label = QLabel(str(self.title))

        self.label.setObjectName("slider_field_label")

        self.label.setWordWrap(True)

        # Current Value Badge

        self.value_label = QLabel("0")

        self.value_label.setObjectName("slider_value_badge")

        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value_label.setMinimumWidth(48)
        self.value_label.setMinimumHeight(30)

        # Header Assembly

        header_layout.addWidget(
            self.label,
            1,
        )

        header_layout.addWidget(
            self.value_label,
            0,
        )

        container_layout.addLayout(header_layout)

        # =====================
        # PREMIUM SLIDER
        # =====================

        self.slider = QSlider(Qt.Orientation.Horizontal)

        self.slider.setObjectName("premium_slider")

        self.slider.setRange(
            minimum,
            maximum,
        )

        self.slider.setMinimumHeight(30)

        self.slider.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.slider.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.slider.setTickPosition(QSlider.TickPosition.NoTicks)

        self.slider.setCursor(Qt.CursorShape.PointingHandCursor)

        self.slider.setAccessibleName(str(self.title))

        self.label.setBuddy(self.slider)

        # Set initial value before connecting
        # the signal to avoid initial emission.

        self.slider.setValue(default)

        self.value_label.setText(str(self.slider.value()))

        container_layout.addWidget(self.slider)

        # =====================
        # RANGE INDICATORS
        # =====================

        range_layout = QHBoxLayout()

        range_layout.setContentsMargins(2, 0, 2, 0)
        range_layout.setSpacing(8)

        self.minimum_label = QLabel(str(self.slider.minimum()))

        self.minimum_label.setObjectName("slider_range_label")

        self.maximum_label = QLabel(str(self.slider.maximum()))

        self.maximum_label.setObjectName("slider_range_label")

        self.maximum_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        range_layout.addWidget(self.minimum_label)

        range_layout.addStretch()

        range_layout.addWidget(self.maximum_label)

        container_layout.addLayout(range_layout)

        # =====================
        # ASSEMBLE COMPONENT
        # =====================

        main_layout.addWidget(self.container)

        # =====================
        # SIGNAL CONNECTION
        # =====================

        self.slider.valueChanged.connect(self.update_value)

        self.update_tooltip(self.slider.value())

    # =====================
    # VALUE CHANGED
    # =====================

    def update_value(self, value):
        self.value_label.setText(str(value))

        self.update_tooltip(value)

        self.value_changed.emit(value)

    # =====================
    # TOOLTIP
    # =====================

    def update_tooltip(self, value):
        self.slider.setToolTip(f"{self.title}: {value}")

    # =====================
    # GET CURRENT VALUE
    # =====================

    def value(self):
        return self.slider.value()

    # =====================
    # SET CURRENT VALUE
    # =====================

    def set_value(self, value):
        self.slider.setValue(int(value))

    # =====================
    # OPTIONAL RANGE UPDATE
    # =====================

    def set_range(
        self,
        minimum,
        maximum,
    ):
        self.slider.setRange(
            minimum,
            maximum,
        )

        self.minimum_label.setText(str(self.slider.minimum()))

        self.maximum_label.setText(str(self.slider.maximum()))

        self.value_label.setText(str(self.slider.value()))

        self.update_tooltip(self.slider.value())

    # =====================
    # PREMIUM STYLING
    # =====================

    def apply_styles(self):
        self.setStyleSheet(
            """
            /* =========================
               MAIN COMPONENT
            ========================= */

            QWidget#slider_field {
                background: transparent;
                border: none;
            }

            /* =========================
               FIELD CONTAINER
            ========================= */

            QFrame#slider_field_container {
                background-color: #1b2940;

                border: 1px solid #304259;
                border-radius: 11px;
            }

            QFrame#slider_field_container:hover {
                background-color: #1e2d44;

                border: 1px solid #426273;
            }

            QFrame#slider_field_container:disabled {
                background-color: #151e2d;

                border: 1px solid #253348;
            }

            /* =========================
               FIELD TITLE
            ========================= */

            QLabel#slider_field_label {
                color: #d5deea;

                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 600;
            }

            QLabel#slider_field_label:disabled {
                color: #64748b;
            }

            /* =========================
               VALUE BADGE
            ========================= */

            QLabel#slider_value_badge {
                background-color: #173a40;

                color: #5eead4;

                border: 1px solid #285d60;
                border-radius: 8px;

                padding: 4px 10px;

                font-family: "Segoe UI";
                font-size: 12px;
                font-weight: 700;
            }

            QLabel#slider_value_badge:disabled {
                background-color: #202b3b;

                color: #64748b;

                border: 1px solid #354459;
            }

            /* =========================
               SLIDER BASE
            ========================= */

            QSlider#premium_slider {
                background: transparent;
                border: none;
            }

            /* =========================
               SLIDER TRACK
            ========================= */

            QSlider#premium_slider::groove:horizontal {
                background-color: #304259;

                height: 6px;

                border: none;
                border-radius: 3px;
            }

            /* =========================
               ACTIVE PROGRESS TRACK
            ========================= */

            QSlider#premium_slider::sub-page:horizontal {
                background-color: #5eead4;

                border: none;
                border-radius: 3px;
            }

            /* =========================
               INACTIVE TRACK
            ========================= */

            QSlider#premium_slider::add-page:horizontal {
                background-color: #304259;

                border: none;
                border-radius: 3px;
            }

            /* =========================
               SLIDER HANDLE
            ========================= */

            QSlider#premium_slider::handle:horizontal {
                background-color: #5eead4;

                border: 3px solid #101b2d;
                border-radius: 11px;

                width: 16px;
                height: 16px;

                margin: -8px 0;
            }

            /* =========================
               HANDLE HOVER
            ========================= */

            QSlider#premium_slider::handle:horizontal:hover {
                background-color: #99f6e4;

                border: 3px solid #173a40;
            }

            /* =========================
               HANDLE PRESSED
            ========================= */

            QSlider#premium_slider::handle:horizontal:pressed {
                background-color: #2dd4bf;

                border: 3px solid #285d60;
            }

            /* =========================
               KEYBOARD FOCUS
            ========================= */

            QSlider#premium_slider:focus::handle:horizontal {
                background-color: #99f6e4;

                border: 3px solid #285d60;
            }

            /* =========================
               DISABLED SLIDER
            ========================= */

            QSlider#premium_slider::groove:horizontal:disabled {
                background-color: #263348;
            }

            QSlider#premium_slider::sub-page:horizontal:disabled {
                background-color: #42615f;
            }

            QSlider#premium_slider::add-page:horizontal:disabled {
                background-color: #263348;
            }

            QSlider#premium_slider::handle:horizontal:disabled {
                background-color: #64748b;

                border: 3px solid #202b3b;
            }

            /* =========================
               MINIMUM / MAXIMUM LABELS
            ========================= */

            QLabel#slider_range_label {
                color: #64748b;

                background: transparent;
                border: none;

                font-family: "Segoe UI";
                font-size: 10px;
                font-weight: 500;
            }

            QLabel#slider_range_label:disabled {
                color: #475569;
            }
            """
        )
